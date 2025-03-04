from flask_babel import lazy_gettext as _l, _, ngettext
from flask_wtf.csrf import generate_csrf
from pydantic import validator
from pydantic.main import BaseModel
from wtforms.validators import InputRequired

from app.forms import SteuerlotseBaseForm
from app.forms.fields import YesNoField
from app.forms.steps.lotse.lotse_step import LotseFormSteuerlotseStep
from app.forms.steps.lotse.personal_data import ShowPersonBPrecondition
from app.forms.steps.lotse.utils import get_number_of_users
from app.forms.steps.lotse_multistep_flow_steps.personal_data_steps import StepFamilienstand
from app.forms.steps.step import SectionLink
from app.model.components import HasDisabilityPersonBProps, HasDisabilityPersonAProps
from app.model.components.helpers import form_fields_dict
from app.templates.react_template import render_react_template

from app.config import Config


class StepDisabilityPersonB(LotseFormSteuerlotseStep):
    name = 'has_disability_person_b'
    label = _l('form.lotse.has_disability.label_person_b')
    section_link = SectionLink('mandatory_data', StepFamilienstand.name, _l('form.lotse.mandatory_data.label'))

    preconditions = [ShowPersonBPrecondition]

    class InputForm(SteuerlotseBaseForm):
        person_b_has_disability = YesNoField(
            render_kw={'data_label': _l('form.lotse.has_disability.data_label')},
            validators=[InputRequired(_l('validate.input-required'))])

    @classmethod
    def get_label(cls, data):
        return cls.label

    def render(self):
        props_dict = HasDisabilityPersonBProps(
            step_header={
                'title': _('form.lotse.person_b.has_disability.title'),
            },
            form={
                'action': self.render_info.submit_url,
                'csrf_token': generate_csrf(),
                'show_overview_button': bool(self.render_info.overview_url),
            },
            fields=form_fields_dict(self.render_info.form),
            prev_url=self.render_info.prev_url,
            plausible_domain=Config.PLAUSIBLE_DOMAIN
        ).camelized_dict()

        return render_react_template(component='HasDisabilityPersonBPage',
                                     props=props_dict,
                                     form=self.render_info.form,
                                     header_title=_('form.lotse.header-title'))


class StepDisabilityPersonA(LotseFormSteuerlotseStep):
    name = 'has_disability_person_a'
    section_link = SectionLink('mandatory_data', StepFamilienstand.name, _l('form.lotse.mandatory_data.label'))

    class InputForm(SteuerlotseBaseForm):
        person_a_has_disability = YesNoField(
            render_kw={'data_label': _l('form.lotse.has_disability.data_label')},
            validators=[InputRequired(_l('validate.input-required'))])

    @classmethod
    def get_label(cls, data=None):
        return ngettext('form.lotse.has_disability.label_person_a', 'form.lotse.has_disability.label_person_a',
                        num=get_number_of_users(data))

    def render(self):
        props_dict = HasDisabilityPersonAProps(
            step_header={
                'title': ngettext('form.lotse.has_disability.title', 'form.lotse.has_disability.title',
                                  num=get_number_of_users(self.stored_data))
            },
            form={
                'action': self.render_info.submit_url,
                'csrf_token': generate_csrf(),
                'show_overview_button': bool(self.render_info.overview_url),
            },
            num_users=get_number_of_users(self.stored_data),
            fields=form_fields_dict(self.render_info.form),
            prev_url=self.render_info.prev_url,
            plausible_domain=Config.PLAUSIBLE_DOMAIN
        ).camelized_dict()

        return render_react_template(component='HasDisabilityPersonAPage',
                                     props=props_dict,
                                     form=self.render_info.form,
                                     header_title=_('form.lotse.header-title'))


class HasDisabilityPersonAPrecondition(BaseModel):
    _step_to_redirect_to = StepDisabilityPersonA.name
    _message_to_flash = _l('form.lotse.skip_reason.has_no_disability')

    person_a_has_disability: str

    @validator('person_a_has_disability', always=True)
    def has_to_be_set_true(cls, v):
        if not v == 'yes':
            raise ValueError
        return v


class HasDisabilityPersonBPrecondition(BaseModel):
    _step_to_redirect_to = StepDisabilityPersonB.name
    _message_to_flash = _l('form.lotse.skip_reason.has_no_disability')

    person_b_has_disability: str

    @validator('person_b_has_disability', always=True)
    def has_to_be_set_true(cls, v):
        if not v == 'yes':
            raise ValueError
        return v
