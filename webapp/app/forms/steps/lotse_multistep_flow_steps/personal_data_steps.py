from app.forms import SteuerlotseBaseForm
from app.forms.steps.step import FormStep, SectionLink
from app.forms.fields import LegacyYesNoField, LegacySteuerlotseDateField, LegacySteuerlotseSelectField, ConfirmationField, \
    SteuerlotseIbanField

from flask_babel import _
from flask_babel import lazy_gettext as _l
from wtforms import RadioField, validators
from wtforms.validators import InputRequired

from app.forms.validations.validators import ValidIban
from app.forms.validations.date_validations import ValidDateOfMarriage, ValidDateOfDeath, ValidDateOfDivorce, ValidDateOfSeparatedSince
from app.model.form_data import show_person_b
from app.utils import get_first_day_of_tax_period


class StepFamilienstand(FormStep):
    name = 'familienstand'

    label = _l('form.lotse.step_familienstand.label')
    section_link = SectionLink('mandatory_data', name, _l('form.lotse.mandatory_data.label'))

    class Form(SteuerlotseBaseForm):
        familienstand = RadioField(
            label=_l('form.lotse.field_familienstand'),
            render_kw={'data_label': _l('form.lotse.field_familienstand.data_label')},
            choices=[
                ('single', _l('form.lotse.familienstand-single')),
                ('married', _l('form.lotse.familienstand-married')),
                ('widowed', _l('form.lotse.familienstand-widowed')),
                ('divorced', _l('form.lotse.familienstand-divorced')),
            ],
            validators=[InputRequired()]
        )
        
        familienstand_date = LegacySteuerlotseDateField(
            label=_l('form.lotse.familienstand_date'),
            render_kw={'data_label': _l('form.lotse.familienstand_date.data_label')},
            prevent_validation_error=True)
        
        familienstand_married_lived_separated = LegacyYesNoField(
            label=_l('form.lotse.familienstand_married_lived_separated'),
            render_kw={'data-example-input': _l('form.lotse.familienstand_married_lived_separated.example_input'),
                       'data_label': _l('form.lotse.familienstand_married_lived_separated.data_label')})
        familienstand_married_lived_separated_since = LegacySteuerlotseDateField(
            label=_l('form.lotse.familienstand_married_lived_separated_since'),
            render_kw={'data_label': _l('form.lotse.familienstand_married_lived_separated_since.data_label')},
            validators=[ValidDateOfSeparatedSince()])
        familienstand_widowed_lived_separated = LegacyYesNoField(
            label=_l('form.lotse.familienstand_widowed_lived_separated'),
            render_kw={'data-example-input': _l('form.lotse.familienstand_widowed_lived_separated.example_input'),
                       'data_label': _l('form.lotse.familienstand_widowed_lived_separated.data_label')})
        familienstand_widowed_lived_separated_since = LegacySteuerlotseDateField(
            label=_l('form.lotse.familienstand_widowed_lived_separated_since'),
            render_kw={'data_label': _l('form.lotse.familienstand_widowed_lived_separated_since.data_label')},
            validators=[ValidDateOfSeparatedSince()])
        familienstand_zusammenveranlagung = LegacyYesNoField(
            label=_l('form.lotse.field_familienstand_zusammenveranlagung'),
            render_kw={'data_label': _l('form.lotse.familienstand_zusammenveranlagung.data_label')})
        familienstand_confirm_zusammenveranlagung = ConfirmationField(
            input_required=False,
            label=_l('form.lotse.familienstand_confirm_zusammenveranlagung'),
            render_kw={'data_label': _l('form.lotse.familienstand_confirm_zusammenveranlagung.data_label')})

        def validate_familienstand_date(self, field):
            if self.familienstand.data == 'single':
                validators.Optional()(self, field)
            elif self.familienstand.data == 'married':
                validators.InputRequired(_l('validate.date-of-marriage-missing'))(self, field)
                ValidDateOfMarriage()(self, field)
            elif self.familienstand.data == 'widowed':
                validators.InputRequired(_l('validate.date-of-death-missing'))(self, field)      
                ValidDateOfDeath()(self, field)  
            elif self.familienstand.data == 'divorced':
                validators.InputRequired(_l('validate.date-of-divorce-missing'))(self, field)
                ValidDateOfDivorce()(self, field) 

        def validate_familienstand_married_lived_separated(self, field):
            if self.familienstand.data == 'married':
                validators.InputRequired(_l('form.lotse.validation-familienstand-married-lived-separated'))(self, field)
            else:
                validators.Optional()(self, field)

        def validate_familienstand_married_lived_separated_since(self, field):
            if self.familienstand.data == 'married' and self.familienstand_married_lived_separated.data == 'yes':
                
                validators.InputRequired(_l('validate.date-of-divorce-missing'))(self, field)
            else:
                validators.Optional()(self, field)
                
            if field.data and self.familienstand_date.data and field.data < self.familienstand_date.data:
                from wtforms.validators import ValidationError
                raise ValidationError(_('form.lotse.validation.married-after-separated'))

        def validate_familienstand_widowed_lived_separated(self, field):
            if self.familienstand.data == 'widowed' and \
                    self.familienstand_date.data and \
                    self.familienstand_date.data >= get_first_day_of_tax_period():
                validators.InputRequired(_l('validate.date-of-death-missing'))(self, field)
            else:
                validators.Optional()(self, field)

        def validate_familienstand_widowed_lived_separated_since(self, field):
            if self.familienstand.data == 'widowed' and self.familienstand_widowed_lived_separated.data == 'yes':
                validators.InputRequired(_l('form.lotse.validation-familienstand-widowed-lived-separated-since'))(self,
                                                                                                                  field)
            else:
                validators.Optional()(self, field)
                
            if field.data and field.data >= self.familienstand_date.data:
                from wtforms.validators import ValidationError
                raise ValidationError(_('form.lotse.validation.widowed-before-separated'))

        def validate_familienstand_zusammenveranlagung(self, field):
            married_separated_recently = self.familienstand.data == 'married' and \
                                         self.familienstand_married_lived_separated.data == 'yes' and \
                                         self.familienstand_married_lived_separated_since.data and \
                                         self.familienstand_married_lived_separated_since.data > get_first_day_of_tax_period()
            widowed_separated_recently = self.familienstand.data == 'widowed' and \
                                         self.familienstand_widowed_lived_separated.data == 'yes' and \
                                         self.familienstand_widowed_lived_separated_since.data and \
                                         self.familienstand_widowed_lived_separated_since.data > get_first_day_of_tax_period()

            if married_separated_recently or widowed_separated_recently:
                validators.InputRequired(_l('form.lotse.validation-familienstand-zusammenveranlagung'))(self, field)
            else:
                validators.Optional()(self, field)

        def validate_familienstand_confirm_zusammenveranlagung(self, field):
            married_not_separated = self.familienstand.data == 'married' and \
                                    self.familienstand_married_lived_separated.data == 'no'
            widowed_recently_not_separated = self.familienstand.data == 'widowed' and \
                                             self.familienstand_date.data and \
                                             self.familienstand_date.data >= get_first_day_of_tax_period() and \
                                             self.familienstand_widowed_lived_separated.data == 'no'

            if married_not_separated or widowed_recently_not_separated:
                validators.InputRequired(_l('form.lotse.validation-familienstand-confirm-zusammenveranlagung'))(self,
                                                                                                                field)
            else:
                validators.Optional()(self, field)

    def __init__(self, **kwargs):
        super(StepFamilienstand, self).__init__(
            title=_l('form.lotse.familienstand-title'),
            form=self.Form,
            **kwargs,
            header_title=_('form.lotse.mandatory_data.header-title'),
            template='lotse/form_familienstand.html'
        )


def get_religion_field():
    return LegacySteuerlotseSelectField(
        label=_l('form.lotse.field_person_religion'),
        choices=[
            ('none', _l('form.lotse.field_person_religion.none')),
            ('ak', _l('form.lotse.field_person_religion.ak')),
            ('ev', _l('form.lotse.field_person_religion.ev')),
            ('er', _l('form.lotse.field_person_religion.er')),
            ('erb', _l('form.lotse.field_person_religion.erb')),
            ('ers', _l('form.lotse.field_person_religion.ers')),
            ('fr', _l('form.lotse.field_person_religion.fr')),
            ('fra', _l('form.lotse.field_person_religion.fra')),
            ('fgm', _l('form.lotse.field_person_religion.fgm')),
            ('fgo', _l('form.lotse.field_person_religion.fgo')),
            ('flb', _l('form.lotse.field_person_religion.flb')),
            ('flp', _l('form.lotse.field_person_religion.flp')),
            ('is', _l('form.lotse.field_person_religion.is')),
            ('irb', _l('form.lotse.field_person_religion.irb')),
            ('iw', _l('form.lotse.field_person_religion.iw')),
            ('ikb', _l('form.lotse.field_person_religion.ikb')),
            ('inw', _l('form.lotse.field_person_religion.inw')),
            ('jgf', _l('form.lotse.field_person_religion.jgf')),
            ('jh', _l('form.lotse.field_person_religion.jh')),
            ('jgh', _l('form.lotse.field_person_religion.jgh')),
            ('jkk', _l('form.lotse.field_person_religion.jkk')),
            ('rk', _l('form.lotse.field_person_religion.rk')),
            ('other', _l('form.lotse.field_person_religion.other'))
        ],
        validators=[InputRequired()],
        render_kw={'help': _l('form.lotse.field_person_religion-help'),
                   'data_label': _l('form.lotse.field_person_religion.data_label')})


class StepIban(FormStep):
    name = 'iban'
    label = _l('form.lotse.step_iban.label')
    section_link = SectionLink('mandatory_data', StepFamilienstand.name, _l('form.lotse.mandatory_data.label'))

    class Form(SteuerlotseBaseForm):
        account_holder = RadioField(
            label=_l('form.lotse.iban.account-holder'),
            render_kw={'data_label': _l('form.lotse.iban.account-holder.data_label')},
            choices=[('person_a', _l('form.lotse.iban.account-holder-person-a')),
                     ('person_b', _l('form.lotse.iban.account-holder-person-b')),
                     ])
        iban = SteuerlotseIbanField(
            label=_l('form.lotse.field_iban'),
            render_kw={'data_label': _l('form.lotse.field_iban.data_label'),
                       'data-example-input': _l('form.lotse.field_iban.example_input'),
                       'max_characters': 25},
            validators=[InputRequired(), ValidIban()],
            filters=[lambda value: value.replace(' ', '') if value else value])

    class FormSingle(SteuerlotseBaseForm):
        is_user_account_holder = ConfirmationField(
            label=_l('form.lotse.field_is_user_account_holder'),
            render_kw={'data_label': _l('form.lotse.field_is_user_account_holder.data_label')})
        iban = SteuerlotseIbanField(
            label=_l('form.lotse.field_iban'),
            render_kw={'data_label': _l('form.lotse.field_iban.data_label'),
                       'data-example-input': _l('form.lotse.field_iban.example_input'),
                       'max_characters': 25},
            validators=[InputRequired(), ValidIban()],
            filters=[lambda value: value.replace(' ', '') if value else value])

    def __init__(self, **kwargs):
        super(StepIban, self).__init__(
            title=_l('form.lotse.iban-title'),
            intro=_l('form.lotse.iban-intro'),
            form=self.Form,
            **kwargs,
            header_title=_('form.lotse.mandatory_data.header-title'),
            template='basis/form_standard.html'
        )

    def create_form(self, request, prefilled_data):
        if not show_person_b(prefilled_data):
            self.form = self.FormSingle

        return super().create_form(request, prefilled_data)
