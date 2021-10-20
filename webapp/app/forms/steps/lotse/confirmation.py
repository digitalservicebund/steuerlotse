import logging

from flask import request, flash

from app.data_access.audit_log_controller import create_audit_log_confirmation_entry
from app.forms import SteuerlotseBaseForm
from app.forms.fields import ConfirmationField
from app.forms.steps.lotse.lotse_step import LotseFormSteuerlotseStep

from flask_babel import lazy_gettext as _l, _

from app.forms.steps.lotse_multistep_flow_steps.confirmation_steps import StepConfirmation
from app.model.form_data import MandatoryFieldMissingValidationError


logger = logging.getLogger(__name__)


class StepSummary(LotseFormSteuerlotseStep):
    name = 'summary'
    title = _l('form.lotse.summary-title')
    intro = _l('form.lotse.summary-intro')
    header_title = _l('form.lotse.summary.header-title')
    template = 'lotse/display_summary.html'
    next_step = StepConfirmation

    class InputForm(SteuerlotseBaseForm):
        confirm_complete_correct = ConfirmationField(label=_l('form.lotse.field_confirm_complete_correct'))

    def _main_handle(self):
        super()._main_handle()
        from app.forms.flows.lotse_flow import LotseMultiStepFlow
        missing_fields = None
        try:
            LotseMultiStepFlow._validate_mandatory_fields(self.stored_data)
        except MandatoryFieldMissingValidationError as e:
            logger.info(f"Mandatory est fields missing: {e.missing_fields}", exc_info=True)
            # prevent flashing the same message two times
            # TODO add parameter to know if it's GET or POST instead of requiring request here
            if request.method == 'GET':
                flash(e.get_message(), 'warn')
            missing_fields = e.missing_fields
            self.render_info.next_url = self.url_for_step(StepSummary.name)
        # TODO move this to a more sensible location!
        multistep_flow = LotseMultiStepFlow(endpoint='lotse')
        self.render_info.additional_info['section_steps'] = multistep_flow._get_overview_data(self.stored_data,
                                                                                              missing_fields)
        self.render_info.overview_url = None

        if not missing_fields and request.method == 'POST' and self.render_info.form.validate():
            create_audit_log_confirmation_entry('Confirmed complete correct data', request.remote_addr,
                                                self.stored_data['idnr'], 'confirm_complete_correct',
                                                self.stored_data['confirm_complete_correct'])
