import copy
import unittest
from datetime import date, datetime
from decimal import Decimal, DecimalException
from unittest.mock import patch, MagicMock

import pytest
import requests
from markupsafe import escape

from app.config import Config
from app.elster_client.elster_client import _generate_est_request_data, _BOOL_KEYS, _DECIMAL_KEYS, \
    _DATE_KEYS, _extract_est_response_data, send_unlock_code_activation_with_elster, \
    send_unlock_code_revocation_with_elster, validate_est_with_elster, send_est_with_elster, _log_address_data, \
    validate_tax_number, TaxDeclarationNotDigitallySigned, send_to_erica
from app.forms.flows.lotse_flow import LotseMultiStepFlow
from app.elster_client.elster_errors import ElsterGlobalError, ElsterGlobalValidationError, \
    ElsterGlobalInitialisationError, ElsterTransferError, ElsterCryptError, ElsterIOError, ElsterPrintError, \
    ElsterNullReturnedError, ElsterUnknownError, ElsterAlreadyRequestedError, ElsterResponseUnexpectedStructure, \
    ElsterProcessNotSuccessful, ElsterRequestIdUnkownError, GeneralEricaError, EricaIsMissingFieldError, \
    ElsterRequestAlreadyRevoked, ElsterInvalidBufaNumberError, ElsterInvalidTaxNumberError, EricaRequestTimeoutError, \
    EricaRequestConnectionError
from app.elster_client.elster_client import send_unlock_code_request_with_elster, \
    check_pyeric_response_for_errors
from app.utils import VERANLAGUNGSJAHR
from tests.elster_client.json_responses.sample_responses import get_json_response
from tests.elster_client.mock_erica import MockErica, MockResponse


class TestSendEst(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, test_request_context):
        self.req = test_request_context

    def setUp(self) -> None:
        self.est_including_json = get_json_response('est_including_responses')
        self.est_without_json = get_json_response('est_without_responses')
        self.empty_response = get_json_response('empty')

        self.est_response_including_responses = MockResponse(self.est_including_json, 200)
        self.est_response_without_responses = MockResponse(self.est_without_json, 200)
        self.valid_form_data = {**LotseMultiStepFlow(None)._DEBUG_DATA[1],
                                **{'idnr': LotseMultiStepFlow(None)._DEBUG_DATA[1]['person_a_idnr']}}

        self.invalid_form_data = copy.deepcopy(self.valid_form_data)
        self.invalid_form_data['person_a_idnr'] = MockErica.INVALID_ID

    def test_if_valid_input_and_return_responses_true_return_correct_response_data(self):
        expected_data = {
            'was_successful': True,
            'pdf': self.est_response_including_responses.json()['pdf'].encode(),
            'transfer_ticket': escape(self.est_including_json['transfer_ticket'])
        }

        with patch('requests.post', side_effect=MockErica.mocked_elster_requests), \
                patch('app.elster_client.elster_client.current_user', MagicMock(is_active=True, is_authenticated=True)), \
                patch('app.elster_client.elster_client._log_address_data'), \
                patch('app.elster_client.elster_client.create_audit_log_entry'):
            actual_returned_data = send_est_with_elster(self.valid_form_data, 'IP')

        self.assertEqual(expected_data, actual_returned_data)

    def test_if_valid_input_and_return_responses_false_return_correct_response_data(self):
        expected_data = {
            'was_successful': True,
            'pdf': self.est_response_including_responses.json()['pdf'].encode(),
            'transfer_ticket': self.est_including_json['transfer_ticket']
        }

        with patch('requests.post', side_effect=MockErica.mocked_elster_requests), \
                patch('app.elster_client.elster_client.current_user', MagicMock(is_active=True, is_authenticated=True)), \
                patch('app.elster_client.elster_client._log_address_data'), \
                patch('app.elster_client.elster_client.create_audit_log_entry'):
            actual_returned_data = send_est_with_elster(self.valid_form_data, 'IP')

        self.assertEqual(expected_data, actual_returned_data)

    def test_if_successful_case_then_generate_audit_log_entry(self):
        with patch('requests.post', side_effect=MockErica.mocked_elster_requests), \
                patch('app.elster_client.elster_client.current_user', MagicMock(is_active=True, is_authenticated=True)), \
                patch('app.elster_client.elster_client._log_address_data'), \
                patch('app.elster_client.elster_client.create_audit_log_entry') as audit_log_fun:
            send_est_with_elster(self.valid_form_data, 'IP')
            audit_log_fun.assert_called()

    def test_if_validation_error_occurred_raise_error(self):
        MockErica.deliver_fail_on_get_job = True
        try:
            with patch('requests.post', side_effect=MockErica.mocked_elster_requests), \
                    patch('app.elster_client.elster_client._log_address_data'), \
                    patch('app.elster_client.elster_client.current_user',
                          MagicMock(is_active=True, is_authenticated=True)):
                send_est_with_elster(self.invalid_form_data, 'IP')
                self.fail("No validation error raised")
        except ElsterGlobalValidationError as e:
            self.assertEqual(get_json_response('validation_error_no_resp_v2')['validation_problems'],
                             e.validation_problems)
        finally:
            MockErica.deliver_fail_on_get_job = False

    def test_if_eric_transfer_error_occurred_raise_error(self):
        MockErica.eric_transfer_error_occurred = True
        MockErica.deliver_fail_on_get_job = True
        try:
            with patch('requests.post', side_effect=MockErica.mocked_elster_requests), \
                    patch('app.elster_client.elster_client.current_user',
                          MagicMock(is_active=True, is_authenticated=True)):
                self.assertRaises(ElsterTransferError, send_est_with_elster, self.valid_form_data, 'IP')
        finally:
            MockErica.eric_transfer_error_occurred = False
            MockErica.deliver_fail_on_get_job = False

    def test_if_eric_error_occurred_raise_error(self):
        MockErica.eric_process_not_successful_error_occurred = True
        MockErica.deliver_fail_on_get_job = True
        try:
            with patch('requests.post', side_effect=MockErica.mocked_elster_requests), \
                    patch('app.elster_client.elster_client.current_user',
                          MagicMock(is_active=True, is_authenticated=True)):
                self.assertRaises(ElsterProcessNotSuccessful, send_est_with_elster, self.valid_form_data, 'IP')
        finally:
            MockErica.eric_process_not_successful_error_occurred = False
            MockErica.deliver_fail_on_get_job = False

    def test_if_fields_missing_raise_error(self):
        data = copy.deepcopy(self.valid_form_data)
        data.pop("familienstand")
        MockErica.deliver_fail_on_get_job = True
        try:
            with patch('requests.post', side_effect=MockErica.mocked_elster_requests), \
                    patch('app.elster_client.elster_client.current_user', MagicMock(is_active=True, is_authenticated=True)), \
                    patch('app.elster_client.elster_client._log_address_data'):
                self.assertRaises(EricaIsMissingFieldError, send_est_with_elster, data, 'IP')
        finally:
            MockErica.deliver_fail_on_get_job = False

    def test_if_invalid_bufa_then_return_error(self):
        MockErica.invalid_bufa_number_error_occurred = True
        MockErica.deliver_fail_on_get_job = True
        try:
            with patch('requests.post', side_effect=MockErica.mocked_elster_requests), \
                    patch('app.elster_client.elster_client._log_address_data'), \
                    patch('app.elster_client.elster_client.current_user',
                          MagicMock(is_active=True, is_authenticated=True)):
                self.assertRaises(ElsterInvalidBufaNumberError, send_est_with_elster, self.valid_form_data, 'IP')
        finally:
            MockErica.invalid_bufa_number_error_occurred = False
            MockErica.deliver_fail_on_get_job = False

    def test_if_invalid_tax_number_then_return_error(self):
        MockErica.invalid_tax_number_error_occurred = True
        MockErica.deliver_fail_on_get_job = True
        try:
            with patch('requests.post', side_effect=MockErica.mocked_elster_requests), \
                    patch('app.elster_client.elster_client._log_address_data'), \
                    patch('app.elster_client.elster_client.current_user',
                          MagicMock(is_active=True, is_authenticated=True)):
                self.assertRaises(ElsterInvalidTaxNumberError, send_est_with_elster, self.valid_form_data, 'IP')
        finally:
            MockErica.invalid_tax_number_error_occurred = False
            MockErica.deliver_fail_on_get_job = False


class TestValidateEst(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, test_request_context):
        self.req = test_request_context

    def setUp(self) -> None:
        self.est_including_json = get_json_response('est_including_responses')
        self.est_without_json = get_json_response('est_without_responses')
        self.empty_response = get_json_response('empty')

        self.est_response_including_responses = MockResponse(self.est_including_json, 200)
        self.est_response_without_responses = MockResponse(self.est_without_json, 200)
        self.valid_form_data = LotseMultiStepFlow(None)._DEBUG_DATA[1]

        self.invalid_form_data = copy.deepcopy(self.valid_form_data)
        self.invalid_form_data['person_a_idnr'] = MockErica.INVALID_ID

    def test_if_valid_input_and_return_responses_true_return_correct_response_data(self):
        expected_data = {
            'was_successful': True,
            'pdf': self.est_response_including_responses.json()['pdf'].encode(),
            'transfer_ticket': escape(self.est_including_json['transfer_ticket']),
            'eric_response': escape(self.est_including_json['eric_response']),
            'server_response': escape(self.est_including_json['server_response'])
        }

        with patch('requests.post', side_effect=MockErica.mocked_elster_requests), \
                patch('app.elster_client.elster_client.current_user', MagicMock(is_active=True, is_authenticated=True)):
            actual_returned_data = validate_est_with_elster(self.valid_form_data, include_elster_responses=True)

        self.assertEqual(expected_data, actual_returned_data)

    def test_if_valid_input_and_return_responses_false_return_correct_response_data(self):
        expected_data = {
            'was_successful': True,
            'pdf': self.est_response_including_responses.json()['pdf'].encode(),
            'transfer_ticket': self.est_including_json['transfer_ticket']
        }

        with patch('requests.post', side_effect=MockErica.mocked_elster_requests), \
                patch('app.elster_client.elster_client.current_user', MagicMock(is_active=True, is_authenticated=True)):
            actual_returned_data = validate_est_with_elster(self.valid_form_data, include_elster_responses=False)

        self.assertEqual(expected_data, actual_returned_data)

    def test_if_validation_error_occurred_raise_error(self):
        try:
            with patch('requests.post', side_effect=MockErica.mocked_elster_requests), \
                    patch('app.elster_client.elster_client.current_user',
                          MagicMock(is_active=True, is_authenticated=True)):
                validate_est_with_elster(self.invalid_form_data, include_elster_responses=False)
                self.fail("No validation error occurred.")
        except ElsterGlobalValidationError as e:
            self.assertEqual(get_json_response('validation_error_no_resp')['detail']['validation_problems'],
                             e.validation_problems)

    def test_if_eric_transfer_error_occurred_raise_error(self):
        MockErica.eric_transfer_error_occurred = True
        try:
            with patch('requests.post', side_effect=MockErica.mocked_elster_requests), \
                    patch('app.elster_client.elster_client.current_user',
                          MagicMock(is_active=True, is_authenticated=True)):
                self.assertRaises(ElsterTransferError, validate_est_with_elster, self.valid_form_data,
                                  include_elster_responses=False)
        finally:
            MockErica.eric_transfer_error_occurred = False

    def test_if_eric_transfer_error_occurred_with_responses_raise_error_with_responses(self):
        MockErica.eric_transfer_error_occurred = True
        try:
            with patch('requests.post', side_effect=MockErica.mocked_elster_requests), \
                    patch('app.elster_client.elster_client.current_user',
                          MagicMock(is_active=True, is_authenticated=True)):
                validate_est_with_elster(self.valid_form_data, include_elster_responses=True)
        except ElsterTransferError as e:
            self.assertEqual(escape(get_json_response('transfer_error_with_resp')['detail']['eric_response']),
                             e.eric_response)
            self.assertEqual(escape(get_json_response('transfer_error_with_resp')['detail']['server_response']),
                             e.server_response)
        finally:
            MockErica.eric_transfer_error_occurred = False

    def test_if_eric_error_occurred_raise_error(self):
        MockErica.eric_process_not_successful_error_occurred = True
        try:
            with patch('requests.post', side_effect=MockErica.mocked_elster_requests), \
                    patch('app.elster_client.elster_client.current_user',
                          MagicMock(is_active=True, is_authenticated=True)):
                self.assertRaises(ElsterProcessNotSuccessful, validate_est_with_elster, self.valid_form_data,
                                  include_elster_responses=False)
        finally:
            MockErica.eric_process_not_successful_error_occurred = False


class TestSendUnlockCodeRequest(unittest.TestCase):

    def setUp(self):
        self.already_available_idnr = '1234567889'
        MockErica.available_idnrs = [(self.already_available_idnr, 'request_id', 'Sesame')]
        self.new_idnr = '987654321'

    def test_if_idnr_new_then_return_correct_json(self):
        with patch('requests.post', side_effect=MockErica.mocked_elster_requests), \
                patch('app.elster_client.elster_client.create_audit_log_entry'):
            actual_returned_json = send_unlock_code_request_with_elster({'idnr': self.new_idnr, 'dob': '1990-12-12'},
                                                                        'IP')
            self.assertIn('taxIdNumber', actual_returned_json)
            self.assertIn('elsterRequestId', actual_returned_json)
            self.assertEqual(self.new_idnr, actual_returned_json['taxIdNumber'])
            self.assertIsNotNone(actual_returned_json['elsterRequestId'])
            self.assertIsNotNone(actual_returned_json['transferticket'])

    def test_if_successful_case_then_generate_audit_log_entry(self):
        with patch('requests.post', side_effect=MockErica.mocked_elster_requests), \
                patch('app.elster_client.elster_client.create_audit_log_entry') as audit_log_fun:
            send_unlock_code_request_with_elster({'idnr': self.new_idnr, 'dob': '1990-12-12'},
                                                 'IP')
            audit_log_fun.assert_called()

    def test_if_idnr_already_used_then_return_error(self):
        MockErica.deliver_fail_on_get_job = True
        try:
            with patch('requests.post', side_effect=MockErica.mocked_elster_requests):

                self.assertRaises(ElsterAlreadyRequestedError, send_unlock_code_request_with_elster,
                                  {'idnr': self.already_available_idnr, 'dob': '1990-12-12'}, 'IP')

        finally:
            MockErica.deliver_fail_on_get_job = False

    def test_if_eric_error_transfer_occurred_then_return_error(self):
        MockErica.eric_transfer_error_occurred = True
        MockErica.deliver_fail_on_get_job = True
        try:
            with patch('requests.post', side_effect=MockErica.mocked_elster_requests):
                self.assertRaises(ElsterTransferError, send_unlock_code_request_with_elster,
                                  {'idnr': self.new_idnr, 'dob': '1990-12-12'}, 'IP')
        finally:
            MockErica.eric_transfer_error_occurred = False
            MockErica.deliver_fail_on_get_job = False

    def test_if_eric_error_occurred_then_return_error(self):
        MockErica.eric_process_not_successful_error_occurred = True
        MockErica.deliver_fail_on_get_job = True
        try:
            with patch('requests.post', side_effect=MockErica.mocked_elster_requests):
                self.assertRaises(ElsterProcessNotSuccessful, send_unlock_code_request_with_elster,
                                  {'idnr': self.new_idnr, 'dob': '1990-12-12'}, 'IP')
        finally:
            MockErica.eric_process_not_successful_error_occurred = False
            MockErica.deliver_fail_on_get_job = False

    def tearDown(self):
        if self.new_idnr in MockErica.available_idnrs:
            MockErica.available_idnrs.remove(self.new_idnr)


class TestSendUnlockCodeActivation(unittest.TestCase):
    def setUp(self):
        self.already_available_idnr = '1234567889'
        self.correct_elster_request_id = 'request_id'
        self.correct_unlock_code = 'Sesame'
        MockErica.available_idnrs.append(
            (self.already_available_idnr, self.correct_elster_request_id, self.correct_unlock_code))
        self.new_idnr = '987654321'

    def test_if_existing_idnr_and_correct_unlock_code_then_return_correct_json(self):
        with patch('requests.post', side_effect=MockErica.mocked_elster_requests), \
                patch('app.elster_client.elster_client.create_audit_log_entry'):
            actual_returned_json = send_unlock_code_activation_with_elster({'idnr': self.already_available_idnr,
                                                                            'unlock_code': self.correct_unlock_code},
                                                                           self.correct_elster_request_id, 'IP')
            self.assertIn('taxIdNumber', actual_returned_json)
            self.assertEqual(self.already_available_idnr, actual_returned_json['taxIdNumber'])

    def test_if_successful_case_then_call_generate_audit_log_entry(self):
        with patch('requests.post', side_effect=MockErica.mocked_elster_requests), \
                patch('app.elster_client.elster_client.create_audit_log_entry') as audit_log_fun:
            send_unlock_code_activation_with_elster({'idnr': self.already_available_idnr,
                                                     'unlock_code': self.correct_unlock_code},
                                                    self.correct_elster_request_id, 'IP')
            audit_log_fun.assert_called()

    def test_if_idnr_not_known_then_return_error(self):
        MockErica.deliver_fail_on_get_job = True
        try:
            with patch('requests.post', side_effect=MockErica.mocked_elster_requests):
                self.assertRaises(ElsterRequestIdUnkownError, send_unlock_code_activation_with_elster,
                                  {'idnr': self.new_idnr, 'unlock_code': self.correct_unlock_code}, 'INCORRECT_REQ_ID',
                                  'IP')
        finally:
            MockErica.deliver_fail_on_get_job = False

    def test_if_unlock_code_wrong_then_return_error(self):
        MockErica.deliver_fail_on_get_job = True
        try:
            with patch('requests.post', side_effect=MockErica.mocked_elster_requests), \
                    patch('app.elster_client.elster_client.create_audit_log_entry'):
                self.assertRaises(ElsterRequestIdUnkownError, send_unlock_code_activation_with_elster,
                                  {'idnr': self.already_available_idnr, 'unlock_code': 'INCORRECT'},
                                  self.correct_elster_request_id, 'IP')
        finally:
            MockErica.deliver_fail_on_get_job = False

    def test_if_eric_error_transfer_occurred_then_return_error(self):
        MockErica.eric_transfer_error_occurred = True
        MockErica.deliver_fail_on_get_job = True
        try:
            with patch('requests.post', side_effect=MockErica.mocked_elster_requests):
                self.assertRaises(ElsterTransferError, send_unlock_code_activation_with_elster,
                                  {'idnr': self.already_available_idnr, 'unlock_code': self.correct_unlock_code},
                                  self.correct_elster_request_id, 'IP')
        finally:
            MockErica.eric_transfer_error_occurred = False
            MockErica.deliver_fail_on_get_job = False

    def test_if_eric_error_occurred_then_return_error(self):
        MockErica.eric_process_not_successful_error_occurred = True
        MockErica.deliver_fail_on_get_job = True
        try:
            with patch('requests.post', side_effect=MockErica.mocked_elster_requests):
                self.assertRaises(ElsterProcessNotSuccessful, send_unlock_code_activation_with_elster,
                                  {'idnr': self.already_available_idnr, 'unlock_code': self.correct_unlock_code},
                                  self.correct_elster_request_id, 'IP')
        finally:
            MockErica.eric_process_not_successful_error_occurred = False
            MockErica.deliver_fail_on_get_job = False

    def tearDown(self):
        if self.new_idnr in MockErica.available_idnrs:
            MockErica.available_idnrs.remove(self.new_idnr)


class TestSendUnlockCodeRevocation(unittest.TestCase):
    def setUp(self):
        self.correct_elster_request_id = 'request_id'
        self.available_idnr = '1234567889'
        MockErica.available_idnrs.append((self.available_idnr, self.correct_elster_request_id, 'Sesame'))
        self.new_idnr = '987654321'

    def test_if_existing_elster_request_id_then_return_correct_json(self):
        with patch('requests.post', side_effect=MockErica.mocked_elster_requests), \
                patch('app.elster_client.elster_client.create_audit_log_entry'):
            actual_returned_json = send_unlock_code_revocation_with_elster(
                {'idnr': self.new_idnr, 'elster_request_id': self.correct_elster_request_id}, 'IP')
            self.assertIn('transferticket', actual_returned_json)
            self.assertIn('elsterRequestId', actual_returned_json)

    def test_if_successful_case_then_generate_audit_log_entry(self):
        with patch('requests.post', side_effect=MockErica.mocked_elster_requests), \
                patch('app.elster_client.elster_client.create_audit_log_entry') as audit_log_fun:
            send_unlock_code_revocation_with_elster(
                {'idnr': self.new_idnr, 'elster_request_id': self.correct_elster_request_id},
                'IP')
            audit_log_fun.assert_called()

    def test_if_elster_request_id_not_known_then_return_error(self):
        MockErica.deliver_fail_on_get_job = True
        try:
            with patch('requests.post', side_effect=MockErica.mocked_elster_requests):
                self.assertRaises(ElsterRequestIdUnkownError, send_unlock_code_revocation_with_elster,
                                  {'idnr': self.new_idnr, 'elster_request_id': 'INCORRECT_REQ_ID'}, 'IP')
        finally:
            MockErica.deliver_fail_on_get_job = False

    def test_if_eric_transfer_error_occurred_then_return_error(self):
        MockErica.eric_transfer_error_occurred = True
        MockErica.deliver_fail_on_get_job = True
        try:
            with patch('requests.post', side_effect=MockErica.mocked_elster_requests):
                self.assertRaises(ElsterTransferError, send_unlock_code_revocation_with_elster,
                                  {'idnr': self.new_idnr, 'elster_request_id': self.correct_elster_request_id}, 'IP')
        finally:
            MockErica.eric_transfer_error_occurred = False
            MockErica.deliver_fail_on_get_job = False

    def test_if_elster_request_already_revoked_then_return_error(self):
        MockErica.request_code_already_revoked_error_occurred = True
        MockErica.deliver_fail_on_get_job = True
        try:
            with patch('requests.post', side_effect=MockErica.mocked_elster_requests):
                self.assertRaises(ElsterRequestAlreadyRevoked, send_unlock_code_revocation_with_elster,
                                  {'idnr': self.new_idnr, 'elster_request_id': self.correct_elster_request_id}, 'IP')
        finally:
            MockErica.request_code_already_revoked_error_occurred = False
            MockErica.deliver_fail_on_get_job = False

    def test_if_eric_error_occurred_then_return_error(self):
        MockErica.eric_process_not_successful_error_occurred = True
        MockErica.deliver_fail_on_get_job = True
        try:
            with patch('requests.post', side_effect=MockErica.mocked_elster_requests):
                self.assertRaises(ElsterProcessNotSuccessful, send_unlock_code_revocation_with_elster,
                                  {'idnr': self.new_idnr, 'elster_request_id': self.correct_elster_request_id}, 'IP')
        finally:
            MockErica.eric_process_not_successful_error_occurred = False
            MockErica.deliver_fail_on_get_job = False

    def tearDown(self):
        if self.new_idnr in MockErica.available_idnrs:
            MockErica.available_idnrs.remove(self.new_idnr)


class TestValidateTaxNumber:

    def test_if_tax_number_is_valid_then_return_true(self):
        state_abbreviation = 'BY'
        tax_number = '19811310010'
        result = validate_tax_number(state_abbreviation, tax_number)

        assert result is True

    def test_if_tax_number_is_invalid_then_return_false(self):
        state_abbreviation = 'BY'
        tax_number = '00000111111'
        MockErica.tax_number_is_invalid = True
        try:
            result = validate_tax_number(state_abbreviation, tax_number)

        finally:
            MockErica.tax_number_is_invalid = False

        assert result is False

    def test_if_erica_throws_error_then_raise_error(self):
        state_abbreviation = 'BY'
        tax_number = '19811310010'
        MockErica.eric_process_not_successful_error_occurred = True
        MockErica.deliver_fail_on_get_job = True
        try:
            with pytest.raises(ElsterUnknownError):
                validate_tax_number(state_abbreviation, tax_number)
        finally:
            MockErica.eric_process_not_successful_error_occurred = False
            MockErica.deliver_fail_on_get_job = False


class TestGenerateEStRequestData(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def attach_fixtures(self, test_request_context):
        self.req = test_request_context

    def test_set_form_data_dict_results_in_dict_with_est_data_field_and_meta_data_field(self):
        form_data = LotseMultiStepFlow(None)._DEBUG_DATA[1]

        with patch('app.elster_client.elster_client.current_user', MagicMock(is_active=True, is_authenticated=True)):
            result = _generate_est_request_data(form_data)

        self.assertIn('est_data', result)
        self.assertIn('meta_data', result)

    def test_set_form_data_dict_results_in_est_data_dict_with_same_keys(self):
        form_data = LotseMultiStepFlow(None)._DEBUG_DATA[1]
        with patch('app.elster_client.elster_client.current_user', MagicMock(is_active=True, is_authenticated=True)):
            result = _generate_est_request_data(form_data)

        for key in form_data.keys():
            self.assertIn(key, result['est_data'])

    def test_yes_str_for_bool_keys_result_in_true(self):
        bool_strs = {}
        for key in _BOOL_KEYS:
            bool_strs[key] = 'yes'
        with patch('app.elster_client.elster_client.current_user', MagicMock(is_active=True, is_authenticated=True)):
            result = _generate_est_request_data(bool_strs)

        for key in _BOOL_KEYS:
            self.assertIsInstance(result['est_data'][key], bool)
            self.assertTrue(result['est_data'][key])

    def test_no_str_for_bool_keys_result_in_false(self):
        bool_strs = {}
        for key in _BOOL_KEYS:
            bool_strs[key] = 'no'
        with patch('app.elster_client.elster_client.current_user', MagicMock(is_active=True, is_authenticated=True)):
            result = _generate_est_request_data(bool_strs)

        for key in _BOOL_KEYS:
            self.assertIsInstance(result['est_data'][key], bool)
            self.assertFalse(result['est_data'][key])

    def test_none_for_bool_keys_result_in_false(self):
        bool_strs = {}
        for key in _BOOL_KEYS:
            bool_strs[key] = None
        with patch('app.elster_client.elster_client.current_user', MagicMock(is_active=True, is_authenticated=True)):
            result = _generate_est_request_data(bool_strs)

        for key in _BOOL_KEYS:
            self.assertIsInstance(result['est_data'][key], bool)
            self.assertFalse(result['est_data'][key])

    def test_float_for_decimal_keys_results_in_decimal(self):
        floats = {}
        for key in _DECIMAL_KEYS:
            floats[key] = 1.2
        with patch('app.elster_client.elster_client.current_user', MagicMock(is_active=True, is_authenticated=True)):
            result = _generate_est_request_data(floats)

        for key in _DECIMAL_KEYS:
            self.assertIsInstance(result['est_data'][key], Decimal)
            self.assertEqual(result['est_data'][key], Decimal(1.2))

    def test_decimal_for_decimal_keys_results_in_decimal(self):
        decimals = {}
        for key in _DECIMAL_KEYS:
            decimals[key] = Decimal(1.2)
        with patch('app.elster_client.elster_client.current_user', MagicMock(is_active=True, is_authenticated=True)):
            result = _generate_est_request_data(decimals)

        for key in _DECIMAL_KEYS:
            self.assertIsInstance(result['est_data'][key], Decimal)
            self.assertEqual(result['est_data'][key], Decimal(1.2))

    def test_str_for_decimal_keys_results_in_decimal(self):
        floats = {}
        for key in _DECIMAL_KEYS:
            floats[key] = '1.2'
        with patch('app.elster_client.elster_client.current_user', MagicMock(is_active=True, is_authenticated=True)):
            result = _generate_est_request_data(floats)

        for key in _DECIMAL_KEYS:
            self.assertIsInstance(result['est_data'][key], Decimal)
            self.assertAlmostEqual(result['est_data'][key], Decimal(1.2))  # rounding error when using str

    def test_none_for_decimal_keys_results_in_none(self):
        decimals = {}
        for key in _DECIMAL_KEYS:
            decimals[key] = None
        with patch('app.elster_client.elster_client.current_user', MagicMock(is_active=True, is_authenticated=True)):
            result = _generate_est_request_data(decimals)

        for key in _DECIMAL_KEYS:
            self.assertIsNone(result['est_data'][key])

    def test_non_decimal_value_for_decimal_keys_results_in_conversion_error(self):
        decimals = {}
        for key in _DECIMAL_KEYS:
            decimals[key] = "This str has no master! This str is a free elf."

        with patch('app.elster_client.elster_client.current_user', MagicMock(is_active=True, is_authenticated=True)):
            self.assertRaises(DecimalException, _generate_est_request_data, decimals)

    def test_correct_date_str_for_date_keys_results_in_date(self):
        dates = {}
        for key in _DATE_KEYS:
            dates[key] = '1963-08-28'
        with patch('app.elster_client.elster_client.current_user', MagicMock(is_active=True, is_authenticated=True)):
            result = _generate_est_request_data(dates)

        for key in _DATE_KEYS:
            self.assertIsInstance(result['est_data'][key], date)
            self.assertEqual(result['est_data'][key], datetime(1963, 8, 28).date())

    def test_incorrect_date_str_for_date_keys_raises_value_error(self):
        dates = {}
        for key in _DATE_KEYS:
            dates[key] = '1963-1963-28'
        with patch('app.elster_client.elster_client.current_user', MagicMock(is_active=True, is_authenticated=True)):
            self.assertRaises(ValueError, _generate_est_request_data, dates)

    def test_none_for_date_keys_raises_value_error(self):
        dates = {}
        for key in _DATE_KEYS:
            dates[key] = None

        with patch('app.elster_client.elster_client.current_user', MagicMock(is_active=True, is_authenticated=True)):
            result = _generate_est_request_data(dates)

        for key in _DATE_KEYS:
            self.assertIsNone(result['est_data'][key])

    def test_not_known_key_results_in_unchanged_value(self):
        unknown_keys = {'first_unknown_key': object(), 'second_unknown_key': 42}

        with patch('app.elster_client.elster_client.current_user', MagicMock(is_active=True, is_authenticated=True)):
            result = _generate_est_request_data(unknown_keys)

        for unknown_key in unknown_keys:
            assert result['est_data'][unknown_key] == unknown_keys[unknown_key]

    def test_set_year_results_in_correct_year_in_result(self):
        with patch('app.elster_client.elster_client.current_user', MagicMock(is_active=True, is_authenticated=True)):
            result = _generate_est_request_data({}, 2010)

        self.assertEqual(result['meta_data']['year'], 2010)

    def test_unset_year_results_in_veranlagungsjahr_year_value(self):
        with patch('app.elster_client.elster_client.current_user', MagicMock(unlock_code_hashed="UNLO-CKCO-DE01")):
            result = _generate_est_request_data({})

        self.assertEqual(result['meta_data']['year'], VERANLAGUNGSJAHR)

    def test_if_user_has_no_unlock_code_then_raise_not_digitally_signed_exception(self):
        with patch('app.elster_client.elster_client.current_user', MagicMock(unlock_code_hashed=None)), \
                pytest.raises(TaxDeclarationNotDigitallySigned):
            _generate_est_request_data({})

    def test_if_user_has_no_unlock_code_then_logout_user_is_called(self):
        with patch('app.elster_client.elster_client.current_user', MagicMock(unlock_code_hashed=None)), \
                patch('flask_login.logout_user') as logout_fun, \
                pytest.raises(TaxDeclarationNotDigitallySigned):
            _generate_est_request_data({})

            logout_fun.assert_called_once()


class TestCheckPyericResponseForErrors(unittest.TestCase):
    def setUp(self):
        self.message = 'I solemnly swear that I am up to no good'
        valid_json = {
            'detail': {
                'code': 0,
                'message': self.message
            }
        }
        self.valid_response = MockResponse(valid_json, 422)

    def test_error_code_1_raises_correct_exception(self):
        self.valid_response.json()['detail']['code'] = 1
        self.assertRaises(ElsterGlobalError, check_pyeric_response_for_errors, self.valid_response)

    def test_error_code_1_raises_given_error_message(self):
        self.valid_response.json()['detail']['code'] = 1
        try:
            check_pyeric_response_for_errors(self.valid_response)
        except ElsterGlobalError as e:
            if e.message != self.message:
                self.fail('check_pyeric_response_for_errors returned unexpected error message.')

    def test_error_code_2_raises_correct_exception(self):
        self.valid_response.json()['detail']['code'] = 2
        self.assertRaises(ElsterGlobalValidationError, check_pyeric_response_for_errors, self.valid_response)

    def test_error_code_2_raises_given_error_message(self):
        self.valid_response.json()['detail']['code'] = 2
        try:
            check_pyeric_response_for_errors(self.valid_response)
        except ElsterGlobalValidationError as e:
            if e.message != self.message:
                self.fail('check_pyeric_response_for_errors returned unexpected error message.')

    def test_error_code_3_raises_correct_exception(self):
        self.valid_response.json()['detail']['code'] = 3
        self.assertRaises(ElsterGlobalInitialisationError, check_pyeric_response_for_errors, self.valid_response)

    def test_error_code_3_raises_given_error_message(self):
        self.valid_response.json()['detail']['code'] = 3
        try:
            check_pyeric_response_for_errors(self.valid_response)
        except ElsterGlobalInitialisationError as e:
            if e.message != self.message:
                self.fail('check_pyeric_response_for_errors returned unexpected error message.')

    def test_error_code_4_raises_correct_exception(self):
        self.valid_response.json()['detail']['code'] = 4
        self.assertRaises(ElsterTransferError, check_pyeric_response_for_errors, self.valid_response)

    def test_error_code_4_raises_given_error_message(self):
        self.valid_response.json()['detail']['code'] = 4
        try:
            check_pyeric_response_for_errors(self.valid_response)
        except ElsterTransferError as e:
            if e.message != self.message:
                self.fail('check_pyeric_response_for_errors returned unexpected error message.')

    def test_error_code_5_raises_correct_exception(self):
        self.valid_response.json()['detail']['code'] = 5
        self.assertRaises(ElsterCryptError, check_pyeric_response_for_errors, self.valid_response)

    def test_error_code_5_raises_given_error_message(self):
        self.valid_response.json()['detail']['code'] = 5
        try:
            check_pyeric_response_for_errors(self.valid_response)
        except ElsterCryptError as e:
            if e.message != self.message:
                self.fail('check_pyeric_response_for_errors returned unexpected error message.')

    def test_error_code_6_raises_correct_exception(self):
        self.valid_response.json()['detail']['code'] = 6
        self.assertRaises(ElsterIOError, check_pyeric_response_for_errors, self.valid_response)

    def test_error_code_6_raises_given_error_message(self):
        self.valid_response.json()['detail']['code'] = 6
        try:
            check_pyeric_response_for_errors(self.valid_response)
        except ElsterIOError as e:
            if e.message != self.message:
                self.fail('check_pyeric_response_for_errors returned unexpected error message.')

    def test_error_code_7_raises_correct_exception(self):
        self.valid_response.json()['detail']['code'] = 7
        self.assertRaises(ElsterPrintError, check_pyeric_response_for_errors, self.valid_response)

    def test_error_code_7_raises_given_error_message(self):
        self.valid_response.json()['detail']['code'] = 7
        try:
            check_pyeric_response_for_errors(self.valid_response)
        except ElsterPrintError as e:
            if e.message != self.message:
                self.fail('check_pyeric_response_for_errors returned unexpected error message.')

    def test_error_code_8_raises_correct_exception(self):
        self.valid_response.json()['detail']['code'] = 8
        self.assertRaises(ElsterNullReturnedError, check_pyeric_response_for_errors, self.valid_response)

    def test_error_code_8_raises_given_error_message(self):
        self.valid_response.json()['detail']['code'] = 8
        try:
            check_pyeric_response_for_errors(self.valid_response)
        except ElsterNullReturnedError as e:
            if e.message != self.message:
                self.fail('check_pyeric_response_for_errors returned unexpected error message.')

    def test_error_code_9_raises_correct_exception(self):
        self.valid_response.json()['detail']['code'] = 9
        self.assertRaises(ElsterAlreadyRequestedError, check_pyeric_response_for_errors, self.valid_response)

    def test_error_code_9_raises_given_error_message(self):
        self.valid_response.json()['detail']['code'] = 9
        try:
            check_pyeric_response_for_errors(self.valid_response)
        except ElsterAlreadyRequestedError as e:
            if e.message != self.message:
                self.fail('check_pyeric_response_for_errors returned unexpected error message.')

    def test_error_code_10_raises_correct_exception(self):
        self.valid_response.json()['detail']['code'] = 10
        self.assertRaises(ElsterRequestIdUnkownError, check_pyeric_response_for_errors, self.valid_response)

    def test_error_code_10_raises_given_error_message(self):
        self.valid_response.json()['detail']['code'] = 10
        try:
            check_pyeric_response_for_errors(self.valid_response)
        except ElsterRequestIdUnkownError as e:
            if e.message != self.message:
                self.fail('check_pyeric_response_for_errors returned unexpected error message.')

    def test_error_code_12_raises_correct_exception(self):
        self.valid_response.json()['detail']['code'] = 12
        self.assertRaises(ElsterInvalidBufaNumberError, check_pyeric_response_for_errors, self.valid_response)

    def test_error_code_13_raises_correct_exception(self):
        self.valid_response.json()['detail']['code'] = 13
        self.assertRaises(ElsterInvalidTaxNumberError, check_pyeric_response_for_errors, self.valid_response)

    def test_unknown_error_code_raises_correct_exception(self):
        self.valid_response.json()['detail']['code'] = 123456543
        self.assertRaises(ElsterUnknownError, check_pyeric_response_for_errors, self.valid_response)

    def test_unknown_error_code_raises_given_error_message(self):
        self.valid_response.json()['detail']['code'] = 123456543
        try:
            check_pyeric_response_for_errors(self.valid_response)
        except ElsterUnknownError as e:
            if e.message != self.message:
                self.fail('check_pyeric_response_for_errors returned unexpected error message.')

    def test_500_error_returns_general_erica_error(self):
        expected_error_message = 'Internal Server Error'
        response_500 = MockResponse(expected_error_message, 500)
        try:
            check_pyeric_response_for_errors(response_500)
        except GeneralEricaError as e:
            if e.message != expected_error_message:
                self.fail('check_pyeric_response_for_errors returned unexpected error message.')

    def test_422_value_error_returns_general_erica_error(self):
        error_json = {'detail': [{'msg': 'An error occurred'}]}
        expected_error_message = str(error_json)
        response_500 = MockResponse(error_json, 422)
        try:
            check_pyeric_response_for_errors(response_500)
        except GeneralEricaError as e:
            if e.message != expected_error_message:
                self.fail('check_pyeric_response_for_errors returned unexpected error message.')


class TestExtractEstResponseData(unittest.TestCase):

    def setUp(self) -> None:
        self.est_including_json = get_json_response('est_including_responses')
        self.est_without_json = get_json_response('est_without_responses')
        self.empty_response = get_json_response('empty')

        self.est_response_including_responses = MockResponse(self.est_including_json, 200)
        self.est_response_without_responses = MockResponse(self.est_without_json, 200)

    def test_if_est_including_responses_then_data_correctly_extracted(self):
        expected_data = {
            'was_successful': True,
            'pdf': self.est_response_including_responses.json()['pdf'].encode(),
            'transfer_ticket': escape(self.est_including_json['transfer_ticket']),
            'eric_response': escape(self.est_including_json['eric_response']),
            'server_response': escape(self.est_including_json['server_response'])
        }

        actual_data = _extract_est_response_data(self.est_response_including_responses)

        self.assertEqual(expected_data, actual_data)

    def test_if_est_without_responses_then_data_correctly_extracted(self):
        expected_data = {
            'was_successful': True,
            'pdf': self.est_response_including_responses.json()['pdf'].encode(),
            'transfer_ticket': self.est_without_json['transfer_ticket']
        }

        actual_data = _extract_est_response_data(self.est_response_without_responses)

        self.assertEqual(expected_data, actual_data)

    def test_if_est_and_session_id_correct_then_set_correct_pdf(self):
        expected_pdf_data = self.est_response_including_responses.json()['pdf'].encode()

        actual_data = _extract_est_response_data(self.est_response_including_responses)

        self.assertEqual(expected_pdf_data, actual_data['pdf'])

    def test_if_est_missing_pdf_then_raise_elster_error(self):
        response_missing_pdf = MockResponse(get_json_response('est_missing_pdf'), 200)

        self.assertRaises(ElsterResponseUnexpectedStructure, _extract_est_response_data, response_missing_pdf)

    def test_if_transfer_ticket_missing_then_raise_elster_error(self):
        response_missing_transfer_ticket = MockResponse(get_json_response('est_missing_transfer_ticket'), 200)

        self.assertRaises(ElsterResponseUnexpectedStructure, _extract_est_response_data,
                          response_missing_transfer_ticket)


class TestLogAddressData(unittest.TestCase):
    def setUp(self):
        self.success_response = MockResponse(get_json_response('get_address_no_resp'), 200)
        self.error_response = MockResponse(get_json_response('insufficient_privileges_no_resp'), 422)

    def test_if_successful_case_then_generate_audit_log_entry(self):
        with patch('requests.post', side_effect=MockErica.mocked_elster_requests), \
                patch('app.elster_client.elster_client.current_user', MagicMock(unlock_code_hashed="UNLO-CKCO-DE01")), \
                patch('app.elster_client.elster_client.send_to_erica', MagicMock(return_value=self.success_response)), \
                patch('app.elster_client.elster_client.create_audit_log_address_entry') as audit_log_fun:
            _log_address_data('IP', '04452397687', {'include_elster_responses': False})
            audit_log_fun.assert_called()

    def test_if_unsuccessful_case_then_raise_transfer_error_and_do_not_generate_audit_log_entry(self):
        with patch('requests.post', side_effect=MockErica.mocked_elster_requests), \
                patch('app.elster_client.elster_client.current_user', MagicMock(unlock_code_hashed="UNLO-CKCO-DE01")), \
                patch('app.elster_client.elster_client.send_to_erica', MagicMock(return_value=self.error_response)), \
                patch('app.elster_client.elster_client.create_audit_log_address_entry') as audit_log_fun:
            self.assertRaises(ElsterTransferError, _log_address_data, 'IP', '04452397687',
                              {'include_elster_responses': False})
            audit_log_fun.assert_not_called()


class TestSendToErica:
    def test_if_erica_timeout_error_occurred_then_raise_corresponding_error(self):
        old_use_mock_api_value = Config.USE_MOCK_API
        Config.USE_MOCK_API = False
        try:
            with patch('requests.post', side_effect=requests.Timeout(response=MockResponse(None, '503'))):
                with pytest.raises(EricaRequestTimeoutError):
                    send_to_erica()
        finally:
            Config.USE_MOCK_API = old_use_mock_api_value

    def test_if_erica_connection_error_occurred_raise_error(self):
        old_use_mock_api_value = Config.USE_MOCK_API
        Config.USE_MOCK_API = False
        try:
            with patch('requests.post', side_effect=requests.ConnectionError(response=MockResponse(None, '504'))):
                with pytest.raises(EricaRequestConnectionError):
                    send_to_erica()
        finally:
            Config.USE_MOCK_API = old_use_mock_api_value

    def test_if_erica_request_error_occurred_raise_error(self):
        old_use_mock_api_value = Config.USE_MOCK_API
        Config.USE_MOCK_API = False
        try:
            with patch('requests.post', side_effect=requests.RequestException(response=MockResponse(None, '500'))):
                with pytest.raises(GeneralEricaError):
                    send_to_erica()
        finally:
            Config.USE_MOCK_API = old_use_mock_api_value
