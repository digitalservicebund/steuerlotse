from decimal import Decimal
from typing import Optional

from flask import render_template
from flask_wtf.csrf import generate_csrf
from pydantic import BaseModel, validator, ValidationError, root_validator
from wtforms import validators, BooleanField

from app.forms import SteuerlotseBaseForm
from app.forms.fields import EuroField, EntriesField, SteuerlotseIntegerField
from app.forms.steps.lotse.confirmation import StepSummary
from app.forms.steps.lotse.lotse_step import LotseFormSteuerlotseStep

from flask_babel import lazy_gettext as _l, _

from app.forms.steps.lotse_multistep_flow_steps.personal_data_steps import StepFamilienstand, StepIban
from app.forms.steps.step import SectionLink
from app.forms.validators import IntegerLength, EURO_FIELD_MAX_LENGTH, NoZero
from app.model.components import SelectStmindProps
from app.model.components.helpers import form_fields_dict
from app.model.form_data import FamilienstandModel, JointTaxesModel


class ShowVorsorgePrecondition(BaseModel):
    stmind_select_vorsorge: str

    @validator('stmind_select_vorsorge', always=True)
    def has_to_be_set_true(cls, v):
        if not v:
            raise ValidationError
        return v


class ShowAussergBelaPrecondition(BaseModel):
    stmind_select_ausserg_bela: str

    @validator('stmind_select_ausserg_bela', always=True)
    def has_to_be_set_true(cls, v):
        if not v:
            raise ValidationError
        return v


class ShowHandwerkerPrecondition(BaseModel):
    stmind_select_handwerker: str

    @validator('stmind_select_handwerker', always=True)
    def has_to_be_set_true(cls, v):
        if not v:
            raise ValidationError
        return v


class ShowSpendenPrecondition(BaseModel):
    stmind_select_spenden: str

    @validator('stmind_select_spenden', always=True)
    def has_to_be_set_true(cls, v):
        if not v:
            raise ValidationError
        return v


class ShowReligionPrecondition(BaseModel):
    stmind_select_religion: str

    @validator('stmind_select_religion', always=True)
    def has_to_be_set_true(cls, v):
        if not v:
            raise ValidationError
        return v


class NotShowPersonBPrecondition(FamilienstandModel):
    @root_validator(skip_on_failure=True)
    def person_b_must_not_be_shown(cls, values):
        if JointTaxesModel.show_person_b(values):
            raise ValidationError
        return values


class HandwerkerHaushaltsnaheSetPrecondition(BaseModel):
    stmind_handwerker_summe: Optional[Decimal]
    stmind_haushaltsnahe_summe: Optional[Decimal]

    @validator('stmind_haushaltsnahe_summe', always=True)
    def one_must_be_set(cls, v, values):
        if not v and ('stmind_handwerker_summe' not in values or not values['stmind_handwerker_summe']):
            raise ValidationError
        return v


class StepSelectStmind(LotseFormSteuerlotseStep):
    name = 'select_stmind'
    title = _l('form.lotse.select_stmind-title')
    intro = _l('form.lotse.select_stmind-intro')
    header_title = _l('form.lotse.steuerminderungen.header-title')
    template = 'react_component.html'
    # TODO remove this once all steps are converted to steuerlotse steps
    prev_step = StepIban

    label = _l('form.lotse.step_select_stmind.label')
    section_link = SectionLink('section_steuerminderung',
                               name,
                               _l('form.lotse.section_steuerminderung.label'))

    @classmethod
    def get_label(cls, data):
        return cls.label

    class InputForm(SteuerlotseBaseForm):
        stmind_select_vorsorge = BooleanField(
            render_kw={'data_label': _l('form.lotse.stmind_select_vorsorge.data_label')})
        stmind_select_ausserg_bela = BooleanField(
            render_kw={'data_label': _l('form.lotse.stmind_select_ausserg_bela.data_label')})
        stmind_select_handwerker = BooleanField(
            render_kw={'data_label': _l('form.lotse.stmind_select_handwerker.data_label')})
        stmind_select_spenden = BooleanField(
            render_kw={'data_label': _l('form.lotse.stmind_select_spenden.data_label')})
        stmind_select_religion = BooleanField(
            render_kw={'data_label': _l('form.lotse.stmind_select_religion.data_label')})

    def render(self, **kwargs):
        props_dict = SelectStmindProps(
            step_header={
                'title': str(self.render_info.step_title),
                'intro': str(self.render_info.step_intro),
            },
            form={
                'action': self.render_info.submit_url,
                'csrf_token': generate_csrf(),
                'show_overview_button': bool(self.render_info.overview_url),
            },
            fields=form_fields_dict(self.render_info.form),
        ).camelized_dict()

        return render_template('react_component.html',
                               component='StmindSelectionPage',
                               props=props_dict,
                               # TODO: These are still required by base.html to set the page title.
                               form=self.form,
                               header_title=self.header_title)


class StepVorsorge(LotseFormSteuerlotseStep):
    name = 'vorsorge'
    title = _l('form.lotse.vorsorge-title')
    intro = _l('form.lotse.vorsorge-intro')
    header_title = _l('form.lotse.steuerminderungen.header-title')
    template = 'lotse/form_aufwendungen_with_list.html'
    preconditions = [ShowVorsorgePrecondition]

    label = _l('form.lotse.step_vorsorge.label')
    section_link = SectionLink('section_steuerminderung',
                               StepSelectStmind.name,
                               _l('form.lotse.section_steuerminderung.label'))

    class InputForm(SteuerlotseBaseForm):
        stmind_vorsorge_summe = EuroField(
            label=_l('form.lotse.field_vorsorge_summe'),
            validators=[IntegerLength(max=EURO_FIELD_MAX_LENGTH)],
            render_kw={'help': _l('form.lotse.field_vorsorge_summe-help'),
                       'data_label': _l('form.lotse.field_vorsorge_summe.data_label')})

    @classmethod
    def get_redirection_step(cls, stored_data):
        if not cls.check_precondition(stored_data):
            return StepSelectStmind.name, _l('form.lotse.skip_reason.steuerminderung_is_no')
        else:
            return None, None

    @classmethod
    def get_label(cls, data):
        return cls.label

    def render(self):
        self.render_info.form.first_field = next(iter(self.render_info.form))
        return render_template(self.template, form=self.render_info.form, render_info=self.render_info,
                               post_list_text=_('form.lotse.vorsorge.post-list-text'),
                               list_items=[
                                        _('form.lotse.vorsorge-list-item-1'),
                                        _('form.lotse.vorsorge-list-item-2'),
                                        _('form.lotse.vorsorge-list-item-3'),
                                    ],
                               header_title=_('form.lotse.steuerminderungen.header-title'))


class StepAussergBela(LotseFormSteuerlotseStep):
    name = 'ausserg_bela'
    title = _l('form.lotse.ausserg_bela-title')
    intro = _l('form.lotse.ausserg_bela-intro')
    header_title = _l('form.lotse.steuerminderungen.header-title')
    template = 'lotse/form_aufwendungen_with_list.html'
    preconditions = [ShowAussergBelaPrecondition]

    label = _l('form.lotse.step_ausserg_bela.label')
    section_link = SectionLink('section_steuerminderung',
                               StepSelectStmind.name, _l('form.lotse.section_steuerminderung.label'))

    class InputForm(SteuerlotseBaseForm):
        stmind_krankheitskosten_summe = EuroField(
            label=_l('form.lotse.field_krankheitskosten_summe'),
            render_kw={'help': _l('form.lotse.field_krankheitskosten-help'),
                       'data_label': _l('form.lotse.field_krankheitskosten_summe.data_label')},
            validators=[IntegerLength(max=EURO_FIELD_MAX_LENGTH)])
        stmind_krankheitskosten_anspruch = EuroField(
            label=_l('form.lotse.field_krankheitskosten_anspruch'),
            render_kw={'data_label': _l('form.lotse.field_krankheitskosten_anspruch.data_label')},
            validators=[IntegerLength(max=EURO_FIELD_MAX_LENGTH)])
        stmind_pflegekosten_summe = EuroField(
            label=_l('form.lotse.field_pflegekosten_summe'),
            render_kw={'help': _l('form.lotse.field_pflegekosten-help'),
                       'data_label': _l('form.lotse.field_pflegekosten_summe.data_label')},
            validators=[IntegerLength(max=EURO_FIELD_MAX_LENGTH)])
        stmind_pflegekosten_anspruch = EuroField(
            label=_l('form.lotse.field_pflegekosten_anspruch'),
            render_kw={'data_label': _l('form.lotse.field_pflegekosten_anspruch.data_label')},
            validators=[IntegerLength(max=EURO_FIELD_MAX_LENGTH)])
        stmind_beh_aufw_summe = EuroField(
            label=_l('form.lotse.field_beh_aufw_summe'),
            render_kw={'help': _l('form.lotse.field_beh_aufw-help'),
                       'data_label': _l('form.lotse.field_beh_aufw_summe.data_label')},
            validators=[IntegerLength(max=EURO_FIELD_MAX_LENGTH)])
        stmind_beh_aufw_anspruch = EuroField(
            label=_l('form.lotse.field_beh_aufw_anspruch'),
            render_kw={'data_label': _l('form.lotse.field_beh_aufw_anspruch.data_label')},
            validators=[IntegerLength(max=EURO_FIELD_MAX_LENGTH)])
        stmind_beh_kfz_summe = EuroField(
            label=_l('form.lotse.field_beh_kfz_summe'),
            render_kw={'help': _l('form.lotse.field_beh_kfz-help'),
                       'data_label': _l('form.lotse.field_beh_kfz_summe.data_label')},
            validators=[IntegerLength(max=EURO_FIELD_MAX_LENGTH)])
        stmind_beh_kfz_anspruch = EuroField(
            label=_l('form.lotse.field_beh_kfz_anspruch'),
            render_kw={'data_label': _l('form.lotse.field_beh_kfz_anspruch.data_label')},
            validators=[IntegerLength(max=EURO_FIELD_MAX_LENGTH)])
        stmind_bestattung_summe = EuroField(
            label=_l('form.lotse.bestattung_summe'),
            render_kw={'help': _l('form.lotse.bestattung-help'),
                       'data_label': _l('form.lotse.bestattung_summe.data_label')},
            validators=[IntegerLength(max=EURO_FIELD_MAX_LENGTH)])
        stmind_bestattung_anspruch = EuroField(
            label=_l('form.lotse.bestattung_anspruch'),
            render_kw={'data_label': _l('form.lotse.bestattung_anspruch.data_label')},
            validators=[IntegerLength(max=EURO_FIELD_MAX_LENGTH)])
        stmind_aussergbela_sonst_summe = EuroField(
            label=_l('form.lotse.aussergbela_sonst_summe'),
            render_kw={'help': _l('form.lotse.aussergbela_sonst-help'),
                       'data_label': _l('form.lotse.aussergbela_sonst_summe.data_label')},
            validators=[IntegerLength(max=EURO_FIELD_MAX_LENGTH)])
        stmind_aussergbela_sonst_anspruch = EuroField(
            label=_l('form.lotse.aussergbela_sonst_anspruch'),
            render_kw={'data_label': _l('form.lotse.aussergbela_sonst_anspruch.data_label')},
            validators=[IntegerLength(max=EURO_FIELD_MAX_LENGTH)])

    @classmethod
    def get_redirection_step(cls, stored_data):
        if not cls.check_precondition(stored_data):
            return StepSelectStmind.name, _l('form.lotse.skip_reason.steuerminderung_is_no')
        else:
            return None, None

    @classmethod
    def get_label(cls, data):
        return cls.label


class StepHaushaltsnaheHandwerker(LotseFormSteuerlotseStep):
    name = 'haushaltsnahe_handwerker'
    title = _l('form.lotse.haushaltsnahe-handwerker-title')
    intro = _l('form.lotse.handwerker-haushaltsnahe-intro')
    header_title = _l('form.lotse.steuerminderungen.header-title')
    template = 'lotse/form_haushaltsnahe_handwerker.html'
    preconditions = [ShowHandwerkerPrecondition]

    label = _l('form.lotse.step_haushaltsnahe_handwerker.label')
    section_link = SectionLink('section_steuerminderung',
                               StepSelectStmind.name, _l('form.lotse.section_steuerminderung.label'))

    class InputForm(SteuerlotseBaseForm):
        stmind_haushaltsnahe_entries = EntriesField(
            label=_l('form.lotse.field_haushaltsnahe_entries'), default=[''],
            validators=[validators.Length(max=999)],
            render_kw={'help': _l('form.lotse.field_haushaltsnahe_entries-help'),
                       'data_label': _l('form.lotse.field_haushaltsnahe_entries.data_label')})
        stmind_haushaltsnahe_summe = EuroField(
            label=_l('form.lotse.field_haushaltsnahe_summe'),
            render_kw={'help': _l('form.lotse.field_haushaltsnahe_summe-help'),
                       'data_label': _l('form.lotse.field_haushaltsnahe_summe.data_label')},
            validators=[IntegerLength(max=EURO_FIELD_MAX_LENGTH)])
        stmind_handwerker_entries = EntriesField(
            label=_l('form.lotse.field_handwerker_entries'), default=[''],
            validators=[validators.Length(max=999)],
            render_kw={'help': _l('form.lotse.field_handwerker_entries-help'),
                       'data_label': _l('form.lotse.field_handwerker_entries.data_label')})
        stmind_handwerker_summe = EuroField(
            label=_l('form.lotse.field_handwerker_summe'),
            render_kw={'help': _l('form.lotse.field_handwerker_summe-help'),
                       'data_label': _l('form.lotse.field_handwerker_summe.data_label')},
            validators=[IntegerLength(max=EURO_FIELD_MAX_LENGTH)])
        stmind_handwerker_lohn_etc_summe = EuroField(
            label=_l('form.lotse.field_handwerker_lohn_etc_summe'),
            render_kw={'data_label': _l('form.lotse.field_handwerker_lohn_etc_summe.data_label')},
            validators=[IntegerLength(max=EURO_FIELD_MAX_LENGTH)])

        def validate_stmind_haushaltsnahe_summe(self, field):
            if SteuerlotseBaseForm._list_has_entries(self.stmind_haushaltsnahe_entries):
                validators.InputRequired(_l('form.lotse.validation-haushaltsnahe-summe'))(self, field)
                NoZero()(self, field)
            else:
                validators.Optional()(self, field)

        def validate_stmind_haushaltsnahe_entries(self, field):
            if self.stmind_haushaltsnahe_summe.data:
                validators.InputRequired(_l('form.lotse.validation-haushaltsnahe-entries'))(self, field)
            else:
                validators.Optional()(self, field)

        def validate_stmind_handwerker_summe(self, field):
            if SteuerlotseBaseForm._list_has_entries(self.stmind_handwerker_entries) or self.stmind_handwerker_lohn_etc_summe.data:
                validators.InputRequired(_l('form.lotse.validation-handwerker-summe'))(self, field)
                NoZero()(self, field)
            else:
                validators.Optional()(self, field)

        def validate_stmind_handwerker_entries(self, field):
            if self.stmind_handwerker_summe.data or self.stmind_handwerker_lohn_etc_summe.data:
                validators.InputRequired(_l('form.lotse.validation-handwerker-entries'))(self, field)
            else:
                validators.Optional()(self, field)

        def validate_stmind_handwerker_lohn_etc_summe(self, field):
            if self.stmind_handwerker_summe.data or SteuerlotseBaseForm._list_has_entries(self.stmind_handwerker_entries):
                validators.InputRequired(_l('form.lotse.validation-handwerker-lohn-etc-summe'))(self, field)
                NoZero()(self, field)
            else:
                validators.Optional()(self, field)

    @classmethod
    def get_redirection_step(cls, stored_data):
        if not cls.check_precondition(stored_data):
            return StepSelectStmind.name, _l('form.lotse.skip_reason.steuerminderung_is_no')
        else:
            return None, None

    @classmethod
    def get_label(cls, data):
        return cls.label

    def render(self):
        self.render_info.form.first_field = next(iter(self.render_info.form))
        return render_template(self.template, form=self.render_info.form, render_info=self.render_info,
                               header_title=_('form.lotse.steuerminderungen.header-title'),
                               input_details_title=_('form.lotse.steuerminderungen.details-title'),
                               input_details_text=_('form.lotse.steuerminderungen.details-text'),
                               details_list_items=[
                                   _l('form.lotse.steuerminderungen.details-list-item-1'),
                                   _l('form.lotse.steuerminderungen.details-list-item-2'),
                                   _l('form.lotse.steuerminderungen.details-list-item-3')
                               ],)


class StepGemeinsamerHaushalt(LotseFormSteuerlotseStep):
    name = 'gem_haushalt'
    title = _l('form.lotse.gem-haushalt-title')
    intro = _l('form.lotse.gem-haushalt-intro')
    header_title = _l('form.lotse.steuerminderungen.header-title')
    template = 'lotse/form_aufwendungen_with_list.html'
    preconditions = [NotShowPersonBPrecondition, ShowHandwerkerPrecondition, HandwerkerHaushaltsnaheSetPrecondition]

    label = _l('form.lotse.step_gem_haushalt.label')
    section_link = SectionLink('section_steuerminderung', StepSelectStmind.name,
                               _l('form.lotse.section_steuerminderung.label'))

    class InputForm(SteuerlotseBaseForm):
        stmind_gem_haushalt_count = SteuerlotseIntegerField(
            label=_l('form.lotse.field_gem_haushalt_count'),
            render_kw={'data_label': _l('form.lotse.field_gem_haushalt_count.data_label')},
            validators=[IntegerLength(max=15)])

        stmind_gem_haushalt_entries = EntriesField(
            label=_l('form.lotse.field_gem_haushalt_entries'),
            render_kw={'help': _l('form.lotse.field_gem_haushalt_entries-help'),
                       'data_label': _l('form.lotse.field_gem_haushalt_entries.data_label')},
            default=[''],
            validators=[validators.Length(max=999)])

        def validate_stmind_gem_haushalt_count(self, field):
            if SteuerlotseBaseForm._list_has_entries(self.stmind_gem_haushalt_entries):
                validators.InputRequired(_l('form.lotse.validation-gem-haushalt-count'))(self, field)
                NoZero()(self, field)
            else:
                validators.Optional()(self, field)

        def validate_stmind_gem_haushalt_entries(self, field):
            if self.stmind_gem_haushalt_count.data and self.stmind_gem_haushalt_count.data != 0:
                validators.InputRequired(_l('form.lotse.validation-gem-haushalt-entries'))(self, field)
            else:
                validators.Optional()(self, field)

    @classmethod
    def get_redirection_step(cls, stored_data):
        # TODO refactor preconditions to hold redirection step?!
        try:
            ShowHandwerkerPrecondition.parse_obj(stored_data)
        except ValidationError:
            return StepSelectStmind.name, _l('form.lotse.skip_reason.steuerminderung_is_no')
        try:
            NotShowPersonBPrecondition.parse_obj(stored_data)
        except ValidationError:
            return StepFamilienstand.name, _l('form.lotse.skip_reason.stmind_gem_haushalt.not-alleinstehend')
        try:
            HandwerkerHaushaltsnaheSetPrecondition.parse_obj(stored_data)
        except ValidationError:
            return StepHaushaltsnaheHandwerker.name, _l('form.lotse.skip_reason.stmind_gem_haushalt.no_handwerker_haushaltsnahe')
        return None, None

    @classmethod
    def get_label(cls, data):
        return cls.label

    def render(self):
        self.render_info.form.first_field = next(iter(self.render_info.form))
        return render_template(self.template, form=self.render_info.form, render_info=self.render_info, list_items=[
            _('form.lotse.gem_haushalt-list-item-1'),
            _('form.lotse.gem_haushalt-list-item-2')
        ], header_title=_('form.lotse.steuerminderungen.header-title'))


class StepReligion(LotseFormSteuerlotseStep):
    name = 'religion'
    title = _l('form.lotse.religion-title')
    intro = _l('form.lotse.religion-intro')
    header_title = _l('form.lotse.steuerminderungen.header-title')
    template = 'lotse/form_aufwendungen_with_list.html'
    preconditions = [ShowReligionPrecondition]

    label = _l('form.lotse.step_religion.label')
    section_link = SectionLink('section_steuerminderung', StepSelectStmind.name,
                               _l('form.lotse.section_steuerminderung.label'))

    class InputForm(SteuerlotseBaseForm):
        stmind_religion_paid_summe = EuroField(
            label=_l('form.lotse.field_religion_paid_summe'),
            validators=[IntegerLength(max=EURO_FIELD_MAX_LENGTH)],
            render_kw={'help': _l('form.lotse.field_religion_paid_summe-help'),
                       'data_label': _l('form.lotse.field_religion_paid_summe.data_label')})
        stmind_religion_reimbursed_summe = EuroField(
            label=_l('form.lotse.field_religion_reimbursed_summe'),
            render_kw={'help': _l('form.lotse.field_religion_reimbursed-help'),
                       'data_label': _l('form.lotse.field_religion_reimbursed_summe.data_label')},
            validators=[IntegerLength(max=EURO_FIELD_MAX_LENGTH)])

    @classmethod
    def get_redirection_step(cls, stored_data):
        if not cls.check_precondition(stored_data):
            return StepSelectStmind.name, _l('form.lotse.skip_reason.steuerminderung_is_no')
        else:
            return None, None

    @classmethod
    def get_label(cls, data):
        return cls.label

    def render(self):
        self.render_info.form.first_field = next(iter(self.render_info.form))
        return render_template(self.template, form=self.render_info.form, render_info=self.render_info, list_items=[],
                               header_title=_('form.lotse.steuerminderungen.header-title'))


class StepSpenden(LotseFormSteuerlotseStep):
    name = 'spenden'
    title = _l('form.lotse.spenden-inland-title')
    intro = _l('form.lotse.spenden-inland-intro')
    header_title = _l('form.lotse.steuerminderungen.header-title')
    template = 'basis/form_standard.html'
    preconditions = [ShowSpendenPrecondition]

    label = _l('form.lotse.step_spenden.label')
    section_link = SectionLink('section_steuerminderung', StepSelectStmind.name, _l('form.lotse.section_steuerminderung.label'))

    class InputForm(SteuerlotseBaseForm):
        stmind_spenden_inland = EuroField(
            label=_l('form.lotse.spenden-inland'),
            validators=[IntegerLength(max=EURO_FIELD_MAX_LENGTH)],
            render_kw={'help': _l('form.lotse.spenden-help'),
                       'data_label': _l('form.lotse.spenden-inland.data_label')})
        stmind_spenden_inland_parteien = EuroField(
            label=_l('form.lotse.spenden-inland-parteien'),
            render_kw={'help': _l('form.lotse.spenden-inland-parteien-help'),
                       'data_label': _l('form.lotse.spenden-inland-parteien.data_label}')},
            validators=[IntegerLength(max=EURO_FIELD_MAX_LENGTH)])

    @classmethod
    def get_redirection_step(cls, stored_data):
        if not cls.check_precondition(stored_data):
            return StepSelectStmind.name, _l('form.lotse.skip_reason.steuerminderung_is_no')
        else:
            return None, None

    @classmethod
    def get_label(cls, data):
        return cls.label
