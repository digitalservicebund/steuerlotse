import logging
from typing import Optional

from app.data_access.user_controller import verify_and_login, activate_user, find_user
from app.data_access.user_controller_errors import UserNotActivatedError, WrongUnlockCodeError, \
    UserNotExistingError
from app.elster_client import elster_client
from app.elster_client.elster_errors import ElsterProcessNotSuccessful
from app.forms.cookie_data import get_data_from_cookie, override_data_in_cookie
from app.forms.flows.multistep_flow import MultiStepFlow
from flask_babel import _
from flask import request, url_for

from app.forms.session_data import get_session_data, override_session_data
from app.forms.steps.unlock_code_activation_steps import UnlockCodeActivationInputStep, \
    UnlockCodeActivationFailureStep


logger = logging.getLogger(__name__)


def _store_id_in_server_session(idnr):
    override_session_data({'idnr': idnr}, 'form_data')


class UnlockCodeActivationMultiStepFlow(MultiStepFlow):
    # TODO: This uses the outdated MultiStepFlow. We do not need a multi step procedure for unlock code activation.
    #  If you adapt the unlock code activation, please consider if you can get rid of the MultiStepFlow.

    _DEBUG_DATA = (
        UnlockCodeActivationInputStep,
        {
            'idnr': '04452397687',
            'unlock_code': 'DBNH-B8JS-9JE7'
        }
    )

    def __init__(self, endpoint):
        super(UnlockCodeActivationMultiStepFlow, self).__init__(
            title=_('form.unlock-code-activation.title'),
            steps=[
                UnlockCodeActivationInputStep,
                UnlockCodeActivationFailureStep
            ],
            endpoint=endpoint,
        )

    # TODO: Use inheritance to clean up this method
    def _handle_specifics_for_step(self, step, render_info, stored_data):
        render_info, stored_data = super(UnlockCodeActivationMultiStepFlow,
                                         self)._handle_specifics_for_step(step, render_info, stored_data)

        if isinstance(step, UnlockCodeActivationInputStep):
            if request.method == 'POST' and render_info.form.validate():
                try:
                    self._login_or_activate_user(stored_data)
                    # prevent going to failure page as in normal flow
                    render_info.next_url = url_for('lotse', step='start')

                    # set idnr also in session
                    _store_id_in_server_session(stored_data['idnr'])

                except (UserNotExistingError, WrongUnlockCodeError, ElsterProcessNotSuccessful):
                    logger.info("Could not activate unlock code for user", exc_info=True)
                    pass  # go to failure step
        elif isinstance(step, UnlockCodeActivationFailureStep):
            render_info.next_url = None

        return render_info, stored_data

    @staticmethod
    def _login_or_activate_user(request_form):
        """
        This will either log in an active user or activate an inactive user if the fsc code is correct

        :param request_form: The form attribute of the request. It should contain an idnr and an unlock_code"""
        idnr = request_form['idnr']
        unlock_code = request_form['unlock_code']
        try:
            verify_and_login(idnr, unlock_code)
        except UserNotActivatedError:
            request_id = find_user(idnr).elster_request_id
            elster_client.send_unlock_code_activation_with_elster(request_form, request_id, request.remote_addr)
            activate_user(idnr, unlock_code)    # If no error is thrown, this result in a problem
            verify_and_login(idnr, unlock_code)

    def _get_session_data(self, ttl: Optional[int] = None):
        return get_data_from_cookie('form_data', ttl)

    def _override_session_data(self, stored_data):
        override_data_in_cookie(data_to_store=stored_data, cookie_data_identifier="form_data")
