from datetime import date
from decimal import Decimal
from typing import Optional

import pytest
from pydantic.main import BaseModel

from erica.request_processing.eric_mapper import EstEricMapping
from erica.request_processing.erica_input import FormDataEst


class DummyInput(BaseModel):

    person_a_disability_degree: Optional[int]
    person_a_has_pflegegrad: Optional[bool]
    person_a_has_merkzeichen_bl: Optional[bool]
    person_a_has_merkzeichen_tbl: Optional[bool]
    person_a_has_merkzeichen_h: Optional[bool]
    person_a_has_merkzeichen_g: Optional[bool]
    person_a_has_merkzeichen_ag: Optional[bool]
    person_a_requests_pauschbetrag: Optional[bool]
    person_a_requests_fahrkostenpauschale: Optional[bool]

    person_b_disability_degree: Optional[int]
    person_b_has_pflegegrad: Optional[bool]
    person_b_has_merkzeichen_bl: Optional[bool]
    person_b_has_merkzeichen_tbl: Optional[bool]
    person_b_has_merkzeichen_h: Optional[bool]
    person_b_has_merkzeichen_g: Optional[bool]
    person_b_has_merkzeichen_ag: Optional[bool]
    person_b_requests_pauschbetrag: Optional[bool]
    person_b_requests_fahrkostenpauschale: Optional[bool]


@pytest.fixture
def standard_est_input_data():

    return FormDataEst(
            submission_without_tax_nr=True,
            bufa_nr='9198',
            bundesland='BY',
            familienstand='married',
            familienstand_date=date(2000, 1, 31),

            person_a_idnr='04452397687',
            person_a_dob=date(1950, 8, 16),
            person_a_first_name='Manfred',
            person_a_last_name='Mustername',
            person_a_street='Steuerweg',
            person_a_street_number=42,
            person_a_plz=20354,
            person_a_town='Hamburg',
            person_a_religion='none',

            person_b_idnr='02293417683',
            person_b_dob=date(1951, 2, 25),
            person_b_first_name='Gerta',
            person_b_last_name='Mustername',
            person_b_same_address=True,
            person_b_religion='rk',

            iban='DE35133713370000012345',
            account_holder='person_a',

            confirm_complete_correct=True,
            confirm_send=True
        )


class TestEstDataPersonAFahrkostenPauschale:

    def test_if_person_a_has_pflegegrad_and_requests_fahrkostenpauschale_then_set_higher_fahrkostenpauschale_for_all_disability_degrees(self, standard_est_input_data):
        disability_degrees = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
        standard_est_input_data.person_a_has_pflegegrad = True
        standard_est_input_data.person_a_requests_fahrkostenpauschale = True

        for disability_degree in disability_degrees:
            standard_est_input_data.person_a_disability_degree = disability_degree

            resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)

            assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_bl_tbl_h_ag_pflegegrad is True
            assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_g_and_degree_70_degree_80 is None

    def test_if_person_a_has_pflegegrad_and_does_not_want_fahrkostenpauschale_then_set_no_fahrkostenpauschale_for_all_disability_degrees(self, standard_est_input_data):
        disability_degrees = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
        standard_est_input_data.person_a_has_pflegegrad = True
        standard_est_input_data.person_a_requests_fahrkostenpauschale = False

        for disability_degree in disability_degrees:
            standard_est_input_data.person_a_disability_degree = disability_degree

            resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)

            assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_bl_tbl_h_ag_pflegegrad is None
            assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_g_and_degree_70_degree_80 is None

    def test_if_person_a_has_merkzeichen_bl_and_requests_fahrkostenpauschale_then_set_higher_fahrkostenpauschale_for_all_disability_degrees(self, standard_est_input_data):
        disability_degrees = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
        standard_est_input_data.person_a_has_merkzeichen_bl = True
        standard_est_input_data.person_a_requests_fahrkostenpauschale = True

        for disability_degree in disability_degrees:
            standard_est_input_data.person_a_disability_degree = disability_degree

            resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)

            assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_bl_tbl_h_ag_pflegegrad is True
            assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_g_and_degree_70_degree_80 is None

    def test_if_person_a_has_merkzeichen_bl_and_does_not_want_fahrkostenpauschale_then_set_no_fahrkostenpauschale_for_all_disability_degrees(self, standard_est_input_data):
        disability_degrees = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
        standard_est_input_data.person_a_has_merkzeichen_bl = True
        standard_est_input_data.person_a_requests_fahrkostenpauschale = False

        for disability_degree in disability_degrees:
            standard_est_input_data.person_a_disability_degree = disability_degree

            resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)

            assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_bl_tbl_h_ag_pflegegrad is None
            assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_g_and_degree_70_degree_80 is None

    def test_if_person_a_has_merkzeichen_tbl_and_requests_fahrkostenpauschale_then_set_higher_fahrkostenpauschale_for_all_disability_degrees(self, standard_est_input_data):
        disability_degrees = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
        standard_est_input_data.person_a_has_merkzeichen_tbl = True
        standard_est_input_data.person_a_requests_fahrkostenpauschale = True

        for disability_degree in disability_degrees:
            standard_est_input_data.person_a_disability_degree = disability_degree

            resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)

            assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_bl_tbl_h_ag_pflegegrad is True
            assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_g_and_degree_70_degree_80 is None

    def test_if_person_a_has_merkzeichen_tbl_and_does_not_want_fahrkostenpauschale_then_set_no_fahrkostenpauschale_for_all_disability_degrees(self, standard_est_input_data):
        disability_degrees = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
        standard_est_input_data.person_a_has_merkzeichen_tbl = True
        standard_est_input_data.person_a_requests_fahrkostenpauschale = False

        for disability_degree in disability_degrees:
            standard_est_input_data.person_a_disability_degree = disability_degree

            resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)

            assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_bl_tbl_h_ag_pflegegrad is None
            assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_g_and_degree_70_degree_80 is None

    def test_if_person_a_has_merkzeichen_h_and_requests_fahrkostenpauschale_then_set_higher_fahrkostenpauschale_for_all_disability_degrees(self, standard_est_input_data):
        disability_degrees = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
        standard_est_input_data.person_a_has_merkzeichen_h = True
        standard_est_input_data.person_a_requests_fahrkostenpauschale = True

        for disability_degree in disability_degrees:
            standard_est_input_data.person_a_disability_degree = disability_degree

            resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)

            assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_bl_tbl_h_ag_pflegegrad is True
            assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_g_and_degree_70_degree_80 is None

    def test_if_person_a_has_merkzeichen_h_and_does_not_want_fahrkostenpauschale_then_set_no_fahrkostenpauschale_for_all_disability_degrees(self, standard_est_input_data):
        disability_degrees = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
        standard_est_input_data.person_a_has_merkzeichen_h = True
        standard_est_input_data.person_a_requests_fahrkostenpauschale = False

        for disability_degree in disability_degrees:
            standard_est_input_data.person_a_disability_degree = disability_degree

            resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)

            assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_bl_tbl_h_ag_pflegegrad is None
            assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_g_and_degree_70_degree_80 is None

    def test_if_person_a_has_merkzeichen_ag_and_requests_fahrkostenpauschale_then_set_higher_fahrkostenpauschale_for_all_disability_degrees(self, standard_est_input_data):
        disability_degrees = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
        standard_est_input_data.person_a_has_merkzeichen_ag = True
        standard_est_input_data.person_a_requests_fahrkostenpauschale = True

        for disability_degree in disability_degrees:
            standard_est_input_data.person_a_disability_degree = disability_degree

            resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)

            assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_bl_tbl_h_ag_pflegegrad is True
            assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_g_and_degree_70_degree_80 is None

    def test_if_person_a_has_merkzeichen_ag_and_does_not_want_fahrkostenpauschale_then_set_no_fahrkostenpauschale_for_all_disability_degrees(self, standard_est_input_data):
        disability_degrees = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
        standard_est_input_data.person_a_has_merkzeichen_ag = True
        standard_est_input_data.person_a_requests_fahrkostenpauschale = False

        for disability_degree in disability_degrees:
            standard_est_input_data.person_a_disability_degree = disability_degree

            resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)

            assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_bl_tbl_h_ag_pflegegrad is None
            assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_g_and_degree_70_degree_80 is None

    def test_if_person_a_has_merkzeichen_g_and_disability_degree_70_and_requests_fahrkostenpauschale_then_set_lower_fahrkostenpauschale(self, standard_est_input_data):
        disability_degree = 70
        standard_est_input_data.person_a_has_merkzeichen_g = True
        standard_est_input_data.person_a_requests_fahrkostenpauschale = True

        standard_est_input_data.person_a_disability_degree = disability_degree

        resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)

        assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_g_and_degree_70_degree_80 is True
        assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_bl_tbl_h_ag_pflegegrad is None

    def test_if_person_a_has_merkzeichen_g_and_disability_degree_70_and_does_not_want_fahrkostenpauschale_then_set_no_fahrkostenpauschale(self, standard_est_input_data):
        disability_degree = 70
        standard_est_input_data.person_a_has_merkzeichen_g = True
        standard_est_input_data.person_a_requests_fahrkostenpauschale = False

        standard_est_input_data.person_a_disability_degree = disability_degree

        resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)

        assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_g_and_degree_70_degree_80 is None
        assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_g_and_degree_70_degree_80 is None

    def test_if_person_a_has_merkzeichen_g_and_disability_degree_below_70_and_requests_fahrkostenpauschale_then_set_no_fahrkostenpauschale(self, standard_est_input_data):
        disability_degree = 65
        standard_est_input_data.person_a_has_merkzeichen_g = True
        standard_est_input_data.person_a_requests_fahrkostenpauschale = True

        standard_est_input_data.person_a_disability_degree = disability_degree

        resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)

        assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_g_and_degree_70_degree_80 is None
        assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_g_and_degree_70_degree_80 is None

    def test_if_a_has_no_merkzeichen_and_disability_degree_80_and_requests_fahrkostenpauschale_then_set_lower_fahrkostenpauschale(self, standard_est_input_data):
        disability_degree = 80
        standard_est_input_data.person_a_requests_fahrkostenpauschale = True

        standard_est_input_data.person_a_disability_degree = disability_degree

        resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)

        assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_g_and_degree_70_degree_80 is True
        assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_bl_tbl_h_ag_pflegegrad is None

    def test_if_a_has_no_merkzeichen_and_disability_degree_80_and_does_not_want_fahrkostenpauschale_then_set_no_fahrkostenpauschale(self, standard_est_input_data):
        disability_degree = 80
        standard_est_input_data.person_a_requests_fahrkostenpauschale = False

        standard_est_input_data.person_a_disability_degree = disability_degree

        resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)

        assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_g_and_degree_70_degree_80 is None
        assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_g_and_degree_70_degree_80 is None

    def test_if_a_has_no_merkzeichen_and_disability_degree_below_80_and_requests_fahrkostenpauschale_then_set_no_fahrkostenpauschale(self, standard_est_input_data):
        disability_degree = 75
        standard_est_input_data.person_a_requests_fahrkostenpauschale = True

        standard_est_input_data.person_a_disability_degree = disability_degree

        resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)

        assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_g_and_degree_70_degree_80 is None
        assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_g_and_degree_70_degree_80 is None


class TestEstDataPersonAPauschbetrag:

    def test_if_person_a_has_merkzeichen_bl_then_set_correct_field(self, standard_est_input_data):
        standard_est_input_data.person_a_has_merkzeichen_bl = True
        resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)
        assert resulting_input_data.person_a_pauschbetrag_has_merkzeichen_bl_tbl_h_pflegegrad is True

    def test_if_person_a_has_merkzeichen_bl_then_do_not_set_other_merkzeichen_field(self, standard_est_input_data):
        standard_est_input_data.person_a_has_merkzeichen_bl = True
        resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)
        assert resulting_input_data.person_a_pauschbetrag_has_merkzeichen_g_ag is None

    def test_if_person_a_has_merkzeichen_tbl_then_set_correct_field(self, standard_est_input_data):
        standard_est_input_data.person_a_has_merkzeichen_tbl = True
        resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)
        assert resulting_input_data.person_a_pauschbetrag_has_merkzeichen_bl_tbl_h_pflegegrad is True

    def test_if_person_a_has_merkzeichen_tbl_then_do_not_set_other_merkzeichen_field(self, standard_est_input_data):
        standard_est_input_data.person_a_has_merkzeichen_tbl = True
        resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)
        assert resulting_input_data.person_a_pauschbetrag_has_merkzeichen_g_ag is None

    def test_if_person_a_has_merkzeichen_h_then_set_correct_field(self, standard_est_input_data):
        standard_est_input_data.person_a_has_merkzeichen_h = True
        resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)
        assert resulting_input_data.person_a_pauschbetrag_has_merkzeichen_bl_tbl_h_pflegegrad is True

    def test_if_person_a_has_merkzeichen_h_then_do_not_set_other_merkzeichen_field(self, standard_est_input_data):
        standard_est_input_data.person_a_has_merkzeichen_h = True
        resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)
        assert resulting_input_data.person_a_pauschbetrag_has_merkzeichen_g_ag is None

    def test_if_person_a_has_pflegegrad_then_set_correct_field(self, standard_est_input_data):
        standard_est_input_data.person_a_has_pflegegrad = True
        resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)
        assert resulting_input_data.person_a_pauschbetrag_has_merkzeichen_bl_tbl_h_pflegegrad is True

    def test_if_person_a_has_pflegegrad_then_do_not_set_other_merkzeichen_field(self, standard_est_input_data):
        standard_est_input_data.person_a_has_pflegegrad = True
        resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)
        assert resulting_input_data.person_a_pauschbetrag_has_merkzeichen_g_ag is None

    def test_if_person_a_has_merkzeichen_g_then_set_correct_field(self, standard_est_input_data):
        standard_est_input_data.person_a_has_merkzeichen_g = True
        resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)
        assert resulting_input_data.person_a_pauschbetrag_has_merkzeichen_g_ag is True

    def test_if_person_a_has_merkzeichen_g_then_do_not_set_other_merkzeichen_field(self, standard_est_input_data):
        standard_est_input_data.person_a_has_merkzeichen_g = True
        resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)
        assert resulting_input_data.person_a_pauschbetrag_has_merkzeichen_bl_tbl_h_pflegegrad is None

    def test_if_person_a_has_merkzeichen_ag_then_set_correct_field(self, standard_est_input_data):
        standard_est_input_data.person_a_has_merkzeichen_ag = True
        resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)
        assert resulting_input_data.person_a_pauschbetrag_has_merkzeichen_g_ag is True

    def test_if_person_a_has_merkzeichen_ag_then_do_not_set_other_merkzeichen_field(self, standard_est_input_data):
        standard_est_input_data.person_a_has_merkzeichen_ag = True
        resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)
        assert resulting_input_data.person_a_pauschbetrag_has_merkzeichen_bl_tbl_h_pflegegrad is None


class TestEstDataPersonBFahrkostenPauschale:

    def test_if_person_b_has_pflegegrad_and_requests_fahrkostenpauschale_then_set_higher_fahrkostenpauschale_for_all_disability_degrees(self, standard_est_input_data):
        disability_degrees = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
        standard_est_input_data.person_b_has_pflegegrad = True
        standard_est_input_data.person_b_requests_fahrkostenpauschale = True

        for disability_degree in disability_degrees:
            standard_est_input_data.person_b_disability_degree = disability_degree

            resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)

            assert resulting_input_data.person_b_fahrkostenpauschale_has_merkzeichen_bl_tbl_h_ag_pflegegrad is True
            assert resulting_input_data.person_b_fahrkostenpauschale_has_merkzeichen_g_and_degree_70_degree_80 is None

    def test_if_person_b_has_pflegegrad_and_does_not_want_fahrkostenpauschale_then_set_no_fahrkostenpauschale_for_all_disability_degrees(self, standard_est_input_data):
        disability_degrees = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
        standard_est_input_data.person_b_has_pflegegrad = True
        standard_est_input_data.person_b_requests_fahrkostenpauschale = False

        for disability_degree in disability_degrees:
            standard_est_input_data.person_b_disability_degree = disability_degree

            resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)

            assert resulting_input_data.person_b_fahrkostenpauschale_has_merkzeichen_bl_tbl_h_ag_pflegegrad is None
            assert resulting_input_data.person_b_fahrkostenpauschale_has_merkzeichen_g_and_degree_70_degree_80 is None

    def test_if_person_b_has_merkzeichen_bl_and_requests_fahrkostenpauschale_then_set_higher_fahrkostenpauschale_for_all_disability_degrees(self, standard_est_input_data):
        disability_degrees = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
        standard_est_input_data.person_b_has_merkzeichen_bl = True
        standard_est_input_data.person_b_requests_fahrkostenpauschale = True

        for disability_degree in disability_degrees:
            standard_est_input_data.person_b_disability_degree = disability_degree

            resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)

            assert resulting_input_data.person_b_fahrkostenpauschale_has_merkzeichen_bl_tbl_h_ag_pflegegrad is True
            assert resulting_input_data.person_b_fahrkostenpauschale_has_merkzeichen_g_and_degree_70_degree_80 is None

    def test_if_person_b_has_merkzeichen_bl_and_does_not_want_fahrkostenpauschale_then_set_no_fahrkostenpauschale_for_all_disability_degrees(self, standard_est_input_data):
        disability_degrees = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
        standard_est_input_data.person_b_has_merkzeichen_bl = True
        standard_est_input_data.person_b_requests_fahrkostenpauschale = False

        for disability_degree in disability_degrees:
            standard_est_input_data.person_b_disability_degree = disability_degree

            resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)

            assert resulting_input_data.person_b_fahrkostenpauschale_has_merkzeichen_bl_tbl_h_ag_pflegegrad is None
            assert resulting_input_data.person_b_fahrkostenpauschale_has_merkzeichen_g_and_degree_70_degree_80 is None

    def test_if_person_b_has_merkzeichen_tbl_and_requests_fahrkostenpauschale_then_set_higher_fahrkostenpauschale_for_all_disability_degrees(self, standard_est_input_data):
        disability_degrees = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
        standard_est_input_data.person_b_has_merkzeichen_tbl = True
        standard_est_input_data.person_b_requests_fahrkostenpauschale = True

        for disability_degree in disability_degrees:
            standard_est_input_data.person_b_disability_degree = disability_degree

            resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)

            assert resulting_input_data.person_b_fahrkostenpauschale_has_merkzeichen_bl_tbl_h_ag_pflegegrad is True
            assert resulting_input_data.person_b_fahrkostenpauschale_has_merkzeichen_g_and_degree_70_degree_80 is None

    def test_if_person_b_has_merkzeichen_tbl_and_does_not_want_fahrkostenpauschale_then_set_no_fahrkostenpauschale_for_all_disability_degrees(self, standard_est_input_data):
        disability_degrees = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
        standard_est_input_data.person_b_has_merkzeichen_tbl = True
        standard_est_input_data.person_b_requests_fahrkostenpauschale = False

        for disability_degree in disability_degrees:
            standard_est_input_data.person_b_disability_degree = disability_degree

            resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)

            assert resulting_input_data.person_b_fahrkostenpauschale_has_merkzeichen_bl_tbl_h_ag_pflegegrad is None
            assert resulting_input_data.person_b_fahrkostenpauschale_has_merkzeichen_g_and_degree_70_degree_80 is None

    def test_if_person_b_has_merkzeichen_h_and_requests_fahrkostenpauschale_then_set_higher_fahrkostenpauschale_for_all_disability_degrees(self, standard_est_input_data):
        disability_degrees = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
        standard_est_input_data.person_a_has_merkzeichen_h = True
        standard_est_input_data.person_a_requests_fahrkostenpauschale = True

        for disability_degree in disability_degrees:
            standard_est_input_data.person_a_disability_degree = disability_degree

            resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)

            assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_bl_tbl_h_ag_pflegegrad is True
            assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_g_and_degree_70_degree_80 is None

    def test_if_person_a_has_merkzeichen_h_and_does_not_want_fahrkostenpauschale_then_set_no_fahrkostenpauschale_for_all_disability_degrees(self, standard_est_input_data):
        disability_degrees = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
        standard_est_input_data.person_a_has_merkzeichen_h = True
        standard_est_input_data.person_a_requests_fahrkostenpauschale = False

        for disability_degree in disability_degrees:
            standard_est_input_data.person_a_disability_degree = disability_degree

            resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)

            assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_bl_tbl_h_ag_pflegegrad is None
            assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_g_and_degree_70_degree_80 is None

    def test_if_person_a_has_merkzeichen_ag_and_requests_fahrkostenpauschale_then_set_higher_fahrkostenpauschale_for_all_disability_degrees(self, standard_est_input_data):
        disability_degrees = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
        standard_est_input_data.person_a_has_merkzeichen_ag = True
        standard_est_input_data.person_a_requests_fahrkostenpauschale = True

        for disability_degree in disability_degrees:
            standard_est_input_data.person_a_disability_degree = disability_degree

            resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)

            assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_bl_tbl_h_ag_pflegegrad is True
            assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_g_and_degree_70_degree_80 is None

    def test_if_person_a_has_merkzeichen_ag_and_does_not_want_fahrkostenpauschale_then_set_no_fahrkostenpauschale_for_all_disability_degrees(self, standard_est_input_data):
        disability_degrees = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
        standard_est_input_data.person_a_has_merkzeichen_ag = True
        standard_est_input_data.person_a_requests_fahrkostenpauschale = False

        for disability_degree in disability_degrees:
            standard_est_input_data.person_a_disability_degree = disability_degree

            resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)

            assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_bl_tbl_h_ag_pflegegrad is None
            assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_g_and_degree_70_degree_80 is None

    def test_if_person_a_has_merkzeichen_g_and_disability_degree_70_and_requests_fahrkostenpauschale_then_set_lower_fahrkostenpauschale(self, standard_est_input_data):
        disability_degree = 70
        standard_est_input_data.person_a_has_merkzeichen_g = True
        standard_est_input_data.person_a_requests_fahrkostenpauschale = True

        standard_est_input_data.person_a_disability_degree = disability_degree

        resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)

        assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_g_and_degree_70_degree_80 is True
        assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_bl_tbl_h_ag_pflegegrad is None

    def test_if_person_a_has_merkzeichen_g_and_disability_degree_70_and_does_not_want_fahrkostenpauschale_then_set_no_fahrkostenpauschale(self, standard_est_input_data):
        disability_degree = 70
        standard_est_input_data.person_a_has_merkzeichen_g = True
        standard_est_input_data.person_a_requests_fahrkostenpauschale = False

        standard_est_input_data.person_a_disability_degree = disability_degree

        resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)

        assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_g_and_degree_70_degree_80 is None
        assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_g_and_degree_70_degree_80 is None

    def test_if_person_a_has_merkzeichen_g_and_disability_degree_below_70_and_requests_fahrkostenpauschale_then_set_no_fahrkostenpauschale(self, standard_est_input_data):
        disability_degree = 65
        standard_est_input_data.person_a_has_merkzeichen_g = True
        standard_est_input_data.person_a_requests_fahrkostenpauschale = True

        standard_est_input_data.person_a_disability_degree = disability_degree

        resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)

        assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_g_and_degree_70_degree_80 is None
        assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_g_and_degree_70_degree_80 is None

    def test_if_a_has_no_merkzeichen_and_disability_degree_80_and_requests_fahrkostenpauschale_then_set_lower_fahrkostenpauschale(self, standard_est_input_data):
        disability_degree = 80
        standard_est_input_data.person_a_requests_fahrkostenpauschale = True

        standard_est_input_data.person_a_disability_degree = disability_degree

        resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)

        assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_g_and_degree_70_degree_80 is True
        assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_bl_tbl_h_ag_pflegegrad is None

    def test_if_a_has_no_merkzeichen_and_disability_degree_80_and_does_not_want_fahrkostenpauschale_then_set_no_fahrkostenpauschale(self, standard_est_input_data):
        disability_degree = 80
        standard_est_input_data.person_a_requests_fahrkostenpauschale = False

        standard_est_input_data.person_a_disability_degree = disability_degree

        resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)

        assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_g_and_degree_70_degree_80 is None
        assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_g_and_degree_70_degree_80 is None

    def test_if_a_has_no_merkzeichen_and_disability_degree_below_80_and_requests_fahrkostenpauschale_then_set_no_fahrkostenpauschale(self, standard_est_input_data):
        disability_degree = 75
        standard_est_input_data.person_a_requests_fahrkostenpauschale = True

        standard_est_input_data.person_a_disability_degree = disability_degree

        resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)

        assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_g_and_degree_70_degree_80 is None
        assert resulting_input_data.person_a_fahrkostenpauschale_has_merkzeichen_g_and_degree_70_degree_80 is None


class TestEstDataPersonBPauschbetrag:

    def test_if_person_b_has_merkzeichen_bl_then_set_correct_field(self, standard_est_input_data):
        standard_est_input_data.person_b_has_merkzeichen_bl = True
        resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)
        assert resulting_input_data.person_b_pauschbetrag_has_merkzeichen_bl_tbl_h_pflegegrad is True

    def test_if_person_b_has_merkzeichen_bl_then_do_not_set_other_merkzeichen_field(self, standard_est_input_data):
        standard_est_input_data.person_b_has_merkzeichen_bl = True
        resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)
        assert resulting_input_data.person_b_pauschbetrag_has_merkzeichen_g_ag is None

    def test_if_person_b_has_merkzeichen_tbl_then_set_correct_field(self, standard_est_input_data):
        standard_est_input_data.person_b_has_merkzeichen_tbl = True
        resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)
        assert resulting_input_data.person_b_pauschbetrag_has_merkzeichen_bl_tbl_h_pflegegrad is True

    def test_if_person_b_has_merkzeichen_tbl_then_do_not_set_other_merkzeichen_field(self, standard_est_input_data):
        standard_est_input_data.person_b_has_merkzeichen_tbl = True
        resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)
        assert resulting_input_data.person_b_pauschbetrag_has_merkzeichen_g_ag is None

    def test_if_person_b_has_merkzeichen_h_then_set_correct_field(self, standard_est_input_data):
        standard_est_input_data.person_b_has_merkzeichen_h = True
        resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)
        assert resulting_input_data.person_b_pauschbetrag_has_merkzeichen_bl_tbl_h_pflegegrad is True

    def test_if_person_b_has_merkzeichen_h_then_do_not_set_other_merkzeichen_field(self, standard_est_input_data):
        standard_est_input_data.person_b_has_merkzeichen_h = True
        resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)
        assert resulting_input_data.person_b_pauschbetrag_has_merkzeichen_g_ag is None

    def test_if_person_b_has_pflegegrad_then_set_correct_field(self, standard_est_input_data):
        standard_est_input_data.person_b_has_pflegegrad = True
        resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)
        assert resulting_input_data.person_b_pauschbetrag_has_merkzeichen_bl_tbl_h_pflegegrad is True

    def test_if_person_b_has_pflegegrad_then_do_not_set_other_merkzeichen_field(self, standard_est_input_data):
        standard_est_input_data.person_b_has_pflegegrad = True
        resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)
        assert resulting_input_data.person_b_pauschbetrag_has_merkzeichen_g_ag is None

    def test_if_person_b_has_merkzeichen_g_then_set_correct_field(self, standard_est_input_data):
        standard_est_input_data.person_b_has_merkzeichen_g = True
        resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)
        assert resulting_input_data.person_b_pauschbetrag_has_merkzeichen_g_ag is True

    def test_if_person_b_has_merkzeichen_g_then_do_not_set_other_merkzeichen_field(self, standard_est_input_data):
        standard_est_input_data.person_b_has_merkzeichen_g = True
        resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)
        assert resulting_input_data.person_b_pauschbetrag_has_merkzeichen_bl_tbl_h_pflegegrad is None

    def test_if_person_b_has_merkzeichen_ag_then_set_correct_field(self, standard_est_input_data):
        standard_est_input_data.person_b_has_merkzeichen_ag = True
        resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)
        assert resulting_input_data.person_b_pauschbetrag_has_merkzeichen_g_ag is True

    def test_if_person_b_has_merkzeichen_ag_then_do_not_set_other_merkzeichen_field(self, standard_est_input_data):
        standard_est_input_data.person_b_has_merkzeichen_ag = True
        resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)
        assert resulting_input_data.person_b_pauschbetrag_has_merkzeichen_bl_tbl_h_pflegegrad is None


class TestEstDataDisabilityDegree:

    def test_if_person_a_disability_degree_below_20_then_do_not_set_disability_degree(self, standard_est_input_data):
        standard_est_input_data.person_a_disability_degree = 15
        resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)
        assert resulting_input_data.person_a_pauschbetrag_disability_degree is None

    def test_if_person_b_disability_degree_below_20_then_do_not_set_disability_degree(self, standard_est_input_data):
        standard_est_input_data.person_b_disability_degree = 15
        resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)
        assert resulting_input_data.person_b_pauschbetrag_disability_degree is None

    def test_if_person_a_disability_degree_20_then_set_disability_degree(self, standard_est_input_data):
        standard_est_input_data.person_a_disability_degree = 20
        resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)
        assert resulting_input_data.person_a_pauschbetrag_disability_degree == 20

    def test_if_person_b_disability_degree_20_then_set_disability_degree(self, standard_est_input_data):
        standard_est_input_data.person_b_disability_degree = 20
        resulting_input_data = EstEricMapping.parse_obj(standard_est_input_data)
        assert resulting_input_data.person_b_pauschbetrag_disability_degree == 20