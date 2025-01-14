import datetime

import pytest
from flask_babel import ngettext, lazy_gettext as _l
from pydantic import ValidationError
from werkzeug.datastructures import ImmutableMultiDict, MultiDict

from app.forms.flows.lotse_step_chooser import LotseStepChooser
from app.forms.steps.lotse.merkzeichen import StepMerkzeichenPersonA, StepMerkzeichenPersonB, \
    HasMerkzeichenPersonAPrecondition, HasMerkzeichenPersonBPrecondition

_POSITIVE_CHECKBOX_VALUE = 'on'  # The value in standard checkboxes is 'on'.


def new_merkzeichen_person_a_step(form_data):
    return LotseStepChooser().get_correct_step(StepMerkzeichenPersonA.name, True, ImmutableMultiDict(form_data))


@pytest.fixture
def test_request_context_with_person_a_disability(new_test_request_context_with_data_in_session):
    with new_test_request_context_with_data_in_session(session_data={'person_a_has_disability': 'yes'}) as req:
        yield req


@pytest.mark.usefixtures('test_request_context_with_person_a_disability')
class TestStepMerkzeichenPersonAValidation:
    @pytest.fixture()
    def valid_form_data(self):
        return {'person_a_has_pflegegrad': 'no'}

    def test_if_has_pflegegrad_not_given_then_fail_validation(self):
        data = MultiDict({})

        form = new_merkzeichen_person_a_step(form_data=data).render_info.form

        assert form.validate() is False

    def test_if_has_pflegegrad_given_then_succ_validation(self):
        data = MultiDict({'person_a_has_pflegegrad': 'no'})

        form = new_merkzeichen_person_a_step(form_data=data).render_info.form

        assert form.validate() is True

    def test_if_disability_degree_has_allowed_value_then_succ_validation(self):
        for allowed_value in [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]:
            data = MultiDict({'person_a_has_pflegegrad': 'no',
                              'person_a_disability_degree': allowed_value})

            form = new_merkzeichen_person_a_step(form_data=data).render_info.form

            assert form.validate() is True

    def test_if_disability_degree_has_not_allowed_value_then_fail_validation(self):
        for not_allowed_value in [21, 105]:
            data = MultiDict({'person_a_has_pflegegrad': 'no',
                              'person_a_disability_degree': not_allowed_value})

            form = new_merkzeichen_person_a_step(form_data=data).render_info.form

            assert form.validate() is False

    def test_if_disability_degree_zero_and_has_no_merkzeichen_g_or_ag_then_succ_validation(self):
        data = MultiDict({'person_a_has_pflegegrad': 'no',
                          'person_a_disability_degree': 0,
                          'person_a_has_merkzeichen_g': False,
                          'person_a_has_merkzeichen_ag': False})
        form = new_merkzeichen_person_a_step(form_data=data).render_info.form

        assert form.validate() is True

    def test_if_disability_degree_below_20_and_not_zero_and_has_no_merkzeichen_g_or_ag_then_fail_validation(self):
        for not_allowed_value in [1, 19]:
            data = MultiDict({'person_a_has_pflegegrad': 'no',
                              'person_a_disability_degree': not_allowed_value,
                              'person_a_has_merkzeichen_g': False,
                              'person_a_has_merkzeichen_ag': False})

            form = new_merkzeichen_person_a_step(form_data=data).render_info.form

            assert form.validate() is False

    def test_if_disability_degree_below_20_and_has_merkzeichen_g_then_fail_validation(self):
        for not_allowed_value in [0, 1, 19]:
            data = MultiDict({'person_a_has_pflegegrad': 'no',
                              'person_a_disability_degree': not_allowed_value,
                              'person_a_has_merkzeichen_g': True})

            form = new_merkzeichen_person_a_step(form_data=data).render_info.form

            assert form.validate() is False

    def test_if_disability_degree_below_20_and_has_merkzeichen_ag_then_fail_validation(self):
        for not_allowed_value in [0, 1, 19]:
            data = MultiDict({'person_a_has_pflegegrad': 'no',
                              'person_a_disability_degree': not_allowed_value,
                              'person_a_has_merkzeichen_ag': True})

            form = new_merkzeichen_person_a_step(form_data=data).render_info.form

            assert form.validate() is False
    
    def test_if_merkzeichen_g_and_ag_and_disability_degree_not_set_then_succ_validation(self, valid_form_data):
        data = MultiDict(valid_form_data)
        form = new_merkzeichen_person_a_step(form_data=data).render_info.form
        assert form.validate() is True

    def test_if_merkzeichen_g_set_and_disability_degree_not_set_then_fail_validation_with_correct_message(self, valid_form_data):
        data = MultiDict({**valid_form_data, **{'person_a_has_merkzeichen_g': _POSITIVE_CHECKBOX_VALUE}})
        form = new_merkzeichen_person_a_step(form_data=data).render_info.form
        assert form.validate() is False
        assert form.errors['person_a_disability_degree'] == [_l('form.lotse.validation-disability_degree.merkzeichen_g_selected.required')]

    def test_if_merkzeichen_g_set_and_disability_degree_set_then_succ_validation(self, valid_form_data):
        data = MultiDict({**valid_form_data, **{'person_a_has_merkzeichen_g': _POSITIVE_CHECKBOX_VALUE, 'person_a_disability_degree': 20}})
        form = new_merkzeichen_person_a_step(form_data=data).render_info.form
        assert form.validate() is True

    def test_if_merkzeichen_ag_set_and_disability_degree_not_set_then_fail_validation_with_correct_message(self, valid_form_data):
        data = MultiDict({**valid_form_data, **{'person_a_has_merkzeichen_ag': _POSITIVE_CHECKBOX_VALUE}})
        form = new_merkzeichen_person_a_step(form_data=data).render_info.form
        assert form.validate() is False
        assert form.errors['person_a_disability_degree'] == [_l('form.lotse.validation-disability_degree.merkzeichen_ag_selected.required')]

    def test_if_merkzeichen_ag_set_and_disability_degree_set_then_succ_validation(self, valid_form_data):
        data = MultiDict({**valid_form_data, **{'person_a_has_merkzeichen_ag': _POSITIVE_CHECKBOX_VALUE, 'person_a_disability_degree': 20}})
        form = new_merkzeichen_person_a_step(form_data=data).render_info.form
        assert form.validate() is True

    def test_if_merkzeichen_g_and_ag_set_and_disability_degree_set_then_succ_validation(self, valid_form_data):
        data = MultiDict({**valid_form_data, **{'person_a_has_merkzeichen_g': _POSITIVE_CHECKBOX_VALUE,
                                                'person_a_has_merkzeichen_ag': _POSITIVE_CHECKBOX_VALUE,
                                                'person_a_disability_degree': 20}})
        form = new_merkzeichen_person_a_step(form_data=data).render_info.form
        assert form.validate() is True

    def test_if_merkzeichen_g_and_ag_not_set_but_disability_degree_set_then_succ_validation(self, valid_form_data):
        data = MultiDict({**valid_form_data, **{'person_a_disability_degree': 20}})
        form = new_merkzeichen_person_a_step(form_data=data).render_info.form
        assert form.validate() is True

    def test_if_merkzeichen_g_set_and_disability_degree_under_20_then_fail_validation(self, valid_form_data):
        data = MultiDict({**valid_form_data, **{'person_a_has_merkzeichen_g': _POSITIVE_CHECKBOX_VALUE, 'person_a_disability_degree': 15}})
        form = new_merkzeichen_person_a_step(form_data=data).render_info.form
        assert form.validate() is False

    def test_if_merkzeichen_ag_set_and_disability_degree_under_20_then_fail_validation(self, valid_form_data):
        data = MultiDict({**valid_form_data, **{'person_a_has_merkzeichen_ag': _POSITIVE_CHECKBOX_VALUE, 'person_a_disability_degree': 15}})
        form = new_merkzeichen_person_a_step(form_data=data).render_info.form
        assert form.validate() is False
        
        
class TestStepMerkzeichenPersonATexts:

    def test_if_multiple_users_then_show_multiple_title(self, new_test_request_context_with_data_in_session):
        expected_step_title = ngettext('form.lotse.merkzeichen_person_a.title', 'form.lotse.merkzeichen_person_a.title',
                                       num=2)
        session_data = {
            'familienstand': 'married',
            'familienstand_date': datetime.date(2000, 1, 31),
            'familienstand_married_lived_separated': 'no',
            'familienstand_confirm_zusammenveranlagung': True,
            'person_a_has_disability': 'yes',
        }

        with new_test_request_context_with_data_in_session(session_data=session_data):
            step = new_merkzeichen_person_a_step({})
            step._pre_handle()

        assert step.title == expected_step_title

    def test_if_multiple_users_then_show_multiple_label(self, new_test_request_context_with_data_in_session):
        expected_step_label = ngettext('form.lotse.merkzeichen_person_a.label', 'form.lotse.merkzeichen_person_a.label',
                                       num=2)
        session_data = {
            'familienstand': 'married',
            'familienstand_date': datetime.date(2000, 1, 31),
            'familienstand_married_lived_separated': 'no',
            'familienstand_confirm_zusammenveranlagung': True,
            'person_a_has_disability': 'yes',
        }

        with new_test_request_context_with_data_in_session(session_data=session_data):
            step = new_merkzeichen_person_a_step({})
            step._pre_handle()

        assert step.label == expected_step_label

    def test_if_single_user_then_show_single_title(self, new_test_request_context_with_data_in_session):
        expected_step_title = ngettext('form.lotse.merkzeichen_person_a.title', 'form.lotse.merkzeichen_person_a.title',
                                       num=1)
        session_data = {
            'familienstand': 'single',
            'person_a_has_disability': 'yes',
        }

        with new_test_request_context_with_data_in_session(session_data=session_data):
            step = new_merkzeichen_person_a_step({})
            step._pre_handle()

        assert step.title == expected_step_title

    def test_if_single_user_then_show_single_label(self, new_test_request_context_with_data_in_session):
        expected_step_label = ngettext('form.lotse.merkzeichen_person_a.label', 'form.lotse.merkzeichen_person_a.label',
                                       num=1)
        session_data = {
            'familienstand': 'single',
            'person_a_has_disability': 'yes',
        }

        with new_test_request_context_with_data_in_session(session_data=session_data):
            step = new_merkzeichen_person_a_step({})
            step._pre_handle()

        assert step.label == expected_step_label


def new_merkzeichen_person_b_step(form_data):
    return LotseStepChooser().get_correct_step(StepMerkzeichenPersonB.name, True, ImmutableMultiDict(form_data))


@pytest.fixture
def test_post_request_context_with_person_b_disability(new_test_request_context_with_data_in_session):
    with new_test_request_context_with_data_in_session(method="POST", session_data={'person_b_has_disability': 'yes'}) as req:
        yield req


@pytest.mark.usefixtures('test_post_request_context_with_person_b_disability')
class TestStepMerkzeichenPersonBValidation:
    @pytest.fixture()
    def valid_form_data(self):
        return {'person_b_has_pflegegrad': 'no'}

    def test_if_has_pflegegrad_not_given_then_fail_validation(self):
        data = MultiDict({})
        form = new_merkzeichen_person_b_step(form_data=data).render_info.form
        assert form.validate() is False

    def test_if_has_pflegegrad_given_then_succ_validation(self):
        data = MultiDict({'person_b_has_pflegegrad': 'no'})
        form = new_merkzeichen_person_b_step(form_data=data).render_info.form
        assert form.validate() is True

    def test_if_disability_degree_has_allowed_value_then_succ_validation(self):
        for allowed_value in [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]:
            data = MultiDict({'person_b_has_pflegegrad': 'no', 'person_b_disability_degree': allowed_value})
            form = new_merkzeichen_person_b_step(form_data=data).render_info.form
            assert form.validate() is True

    def test_if_disability_degree_has_not_allowed_value_then_fail_validation(self):
        for not_allowed_value in [21, 105]:
            data = MultiDict({'person_b_has_pflegegrad': 'no',
                              'person_b_disability_degree': not_allowed_value})
            form = new_merkzeichen_person_b_step(form_data=data).render_info.form
            assert form.validate() is False

    def test_if_disability_degree_zero_and_has_no_merkzeichen_g_or_ag_then_succ_validation(self):
        data = MultiDict({'person_b_has_pflegegrad': 'no',
                          'person_b_disability_degree': 0,
                          'person_b_has_merkzeichen_g': False,
                          'person_b_has_merkzeichen_ag': False})
        form = new_merkzeichen_person_b_step(form_data=data).render_info.form

        assert form.validate() is True

    def test_if_disability_degree_below_20_and_not_zero_and_has_no_merkzeichen_g_or_ag_then_fail_validation(self):
        for not_allowed_value in [1, 19]:
            data = MultiDict({'person_b_has_pflegegrad': 'no',
                              'person_b_disability_degree': not_allowed_value,
                              'person_b_has_merkzeichen_g': False,
                              'person_b_has_merkzeichen_ag': False})

            form = new_merkzeichen_person_b_step(form_data=data).render_info.form

            assert form.validate() is False

    def test_if_disability_degree_below_20_and_has_merkzeichen_g_then_fail_validation(self):
        for not_allowed_value in [0, 1, 19]:
            data = MultiDict({'person_b_has_pflegegrad': 'no',
                              'person_b_disability_degree': not_allowed_value,
                              'person_b_has_merkzeichen_g': True})

            form = new_merkzeichen_person_b_step(form_data=data).render_info.form

            assert form.validate() is False

    def test_if_disability_degree_below_20_and_has_merkzeichen_ag_then_fail_validation(self):
        for not_allowed_value in [0, 1, 19]:
            data = MultiDict({'person_b_has_pflegegrad': 'no',
                              'person_b_disability_degree': not_allowed_value,
                              'person_b_has_merkzeichen_ag': True})

            form = new_merkzeichen_person_b_step(form_data=data).render_info.form

            assert form.validate() is False

    def test_if_merkzeichen_g_and_ag_and_disability_degree_not_set_then_succ_validation(self, valid_form_data):
        data = MultiDict(valid_form_data)
        form = new_merkzeichen_person_b_step(form_data=data).render_info.form
        assert form.validate() is True

    def test_if_merkzeichen_g_set_and_disability_degree_not_set_then_fail_validation_with_correct_message(self, valid_form_data):
        data = MultiDict({**valid_form_data, **{'person_b_has_merkzeichen_g': _POSITIVE_CHECKBOX_VALUE}})
        form = new_merkzeichen_person_b_step(form_data=data).render_info.form
        assert form.validate() is False
        assert form.errors['person_b_disability_degree'] == [_l('form.lotse.validation-disability_degree.merkzeichen_g_selected.required')]

    def test_if_merkzeichen_g_set_and_disability_degree_set_then_succ_validation(self, valid_form_data):
        data = MultiDict({**valid_form_data, **{'person_b_has_merkzeichen_g': _POSITIVE_CHECKBOX_VALUE, 'person_b_disability_degree': 20}})
        form = new_merkzeichen_person_b_step(form_data=data).render_info.form
        assert form.validate() is True

    def test_if_merkzeichen_ag_set_and_disability_degree_not_set_then_fail_validation_with_correct_message(self, valid_form_data):
        data = MultiDict({**valid_form_data, **{'person_b_has_merkzeichen_ag': _POSITIVE_CHECKBOX_VALUE}})
        form = new_merkzeichen_person_b_step(form_data=data).render_info.form
        assert form.validate() is False
        assert form.errors['person_b_disability_degree'] == [_l('form.lotse.validation-disability_degree.merkzeichen_ag_selected.required')]

    def test_if_merkzeichen_ag_set_and_disability_degree_set_then_succ_validation(self, valid_form_data):
        data = MultiDict({**valid_form_data, **{'person_b_has_merkzeichen_ag': _POSITIVE_CHECKBOX_VALUE, 'person_b_disability_degree': 20}})
        form = new_merkzeichen_person_b_step(form_data=data).render_info.form
        assert form.validate() is True

    def test_if_merkzeichen_g_and_ag_set_and_disability_degree_set_then_succ_validation(self, valid_form_data):
        data = MultiDict({**valid_form_data, **{'person_b_has_merkzeichen_g': _POSITIVE_CHECKBOX_VALUE,
                                                'person_b_has_merkzeichen_ag': _POSITIVE_CHECKBOX_VALUE,
                                                'person_b_disability_degree': 20}})
        form = new_merkzeichen_person_b_step(form_data=data).render_info.form
        assert form.validate() is True

    def test_if_merkzeichen_g_and_ag_not_set_but_disability_degree_set_then_succ_validation(self, valid_form_data):
        data = MultiDict({**valid_form_data, **{'person_b_disability_degree': 20}})
        form = new_merkzeichen_person_b_step(form_data=data).render_info.form
        assert form.validate() is True
    
    def test_if_merkzeichen_g_set_and_disability_degree_under_20_then_fail_validation(self, valid_form_data):
        data = MultiDict({**valid_form_data, **{'person_b_has_merkzeichen_g': _POSITIVE_CHECKBOX_VALUE, 'person_b_disability_degree': 15}})
        form = new_merkzeichen_person_b_step(form_data=data).render_info.form
        assert form.validate() is False

    def test_if_merkzeichen_ag_set_and_disability_degree_under_20_then_fail_validation(self, valid_form_data):
        data = MultiDict({**valid_form_data, **{'person_b_has_merkzeichen_ag': _POSITIVE_CHECKBOX_VALUE, 'person_b_disability_degree': 15}})
        form = new_merkzeichen_person_b_step(form_data=data).render_info.form
        assert form.validate() is False


class TestHasMerkzeichenPersonAPrecondition:

    def test_if_person_a_has_no_merkzeichen_set_then_raise_validation_error(self):
        data = {
            'person_a_has_disability': 'yes',
        }
        with pytest.raises(ValidationError):
            HasMerkzeichenPersonAPrecondition.parse_obj(data)

    def test_if_person_a_has_pflegegrad_set_then_do_not_raise_validation_error(self):
        data = {
            'person_a_has_disability': 'yes',
            'person_a_has_pflegegrad': 'yes'
        }
        try:
            HasMerkzeichenPersonAPrecondition.parse_obj(data)
        except ValidationError:
            pytest.fail("Should not raise a validation error")

    def test_if_person_a_disability_degree_set_then_do_not_raise_validation_error(self):
        data = {
            'person_a_has_disability': 'yes',
            'person_a_disability_degree': 20
        }
        try:
            HasMerkzeichenPersonAPrecondition.parse_obj(data)
        except ValidationError:
            pytest.fail("Should not raise a validation error")

    def test_if_person_a_has_merkzeichen_g_set_then_do_not_raise_validation_error(self):
        data = {
            'person_a_has_disability': 'yes',
            'person_a_has_merkzeichen_g': True
        }
        try:
            HasMerkzeichenPersonAPrecondition.parse_obj(data)
        except ValidationError:
            pytest.fail("Should not raise a validation error")

    def test_if_person_a_has_merkzeichen_ag_set_then_do_not_raise_validation_error(self):
        data = {
            'person_a_has_disability': 'yes',
            'person_a_has_merkzeichen_ag': True
        }
        try:
            HasMerkzeichenPersonAPrecondition.parse_obj(data)
        except ValidationError:
            pytest.fail("Should not raise a validation error")

    def test_if_person_a_has_merkzeichen_bl_set_then_do_not_raise_validation_error(self):
        data = {
            'person_a_has_disability': 'yes',
            'person_a_has_merkzeichen_bl': True,
        }
        try:
            HasMerkzeichenPersonAPrecondition.parse_obj(data)
        except ValidationError:
            pytest.fail("Should not raise a validation error")

    def test_if_person_a_has_merkzeichen_tbl_set_then_do_not_raise_validation_error(self):
        data = {
            'person_a_has_disability': 'yes',
            'person_a_has_merkzeichen_tbl': True,
        }
        try:
            HasMerkzeichenPersonAPrecondition.parse_obj(data)
        except ValidationError:
            pytest.fail("Should not raise a validation error")

    def test_if_person_a_has_merkzeichen_h_set_then_do_not_raise_validation_error(self):
        data = {
            'person_a_has_disability': 'yes',
            'person_a_has_merkzeichen_h': True
        }
        try:
            HasMerkzeichenPersonAPrecondition.parse_obj(data)
        except ValidationError:
            pytest.fail("Should not raise a validation error")


class TestHasMerkzeichenPersonBPrecondition:

    def test_if_person_b_has_no_merkzeichen_set_then_raise_validation_error(self):
        data = {
            'person_b_has_disability': 'yes',
        }
        with pytest.raises(ValidationError):
            HasMerkzeichenPersonBPrecondition.parse_obj(data)

    def test_if_person_b_has_pflegegrad_set_then_do_not_raise_validation_error(self):
        data = {
            'person_b_has_disability': 'yes',
            'person_b_has_pflegegrad': 'yes',
        }
        try:
            HasMerkzeichenPersonBPrecondition.parse_obj(data)
        except ValidationError:
            pytest.fail("Should not raise a validation error")

    def test_if_person_b_disability_degree_set_then_do_not_raise_validation_error(self):
        data = {
            'person_b_has_disability': 'yes',
            'person_b_disability_degree': 20,
        }
        try:
            HasMerkzeichenPersonBPrecondition.parse_obj(data)
        except ValidationError:
            pytest.fail("Should not raise a validation error")

    def test_if_person_b_has_merkzeichen_g_set_then_do_not_raise_validation_error(self):
        data = {
            'person_b_has_disability': 'yes',
            'person_b_has_merkzeichen_g': True,
        }
        try:
            HasMerkzeichenPersonBPrecondition.parse_obj(data)
        except ValidationError:
            pytest.fail("Should not raise a validation error")

    def test_if_person_b_has_merkzeichen_ag_set_then_do_not_raise_validation_error(self):
        data = {
            'person_b_has_disability': 'yes',
            'person_b_has_merkzeichen_ag': True,
        }
        try:
            HasMerkzeichenPersonBPrecondition.parse_obj(data)
        except ValidationError:
            pytest.fail("Should not raise a validation error")

    def test_if_person_b_has_merkzeichen_bl_set_then_do_not_raise_validation_error(self):
        data = {
            'person_b_has_disability': 'yes',
            'person_b_has_merkzeichen_bl': True
        }
        try:
            HasMerkzeichenPersonBPrecondition.parse_obj(data)
        except ValidationError:
            pytest.fail("Should not raise a validation error")

    def test_if_person_b_has_merkzeichen_tbl_set_then_do_not_raise_validation_error(self):
        data = {
            'person_b_has_disability': 'yes',
            'person_b_has_merkzeichen_tbl': True,
        }
        try:
            HasMerkzeichenPersonBPrecondition.parse_obj(data)
        except ValidationError:
            pytest.fail("Should not raise a validation error")

    def test_if_person_b_has_merkzeichen_h_set_then_do_not_raise_validation_error(self):
        data = {
            'person_b_has_disability': 'yes',
            'person_b_has_merkzeichen_h': True
        }
        try:
            HasMerkzeichenPersonBPrecondition.parse_obj(data)
        except ValidationError:
            pytest.fail("Should not raise a validation error")