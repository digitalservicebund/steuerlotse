from app.forms.steps.lotse.fahrkostenpauschbetrag import calculate_fahrkostenpauschbetrag


class TestCalculatePauschbetrag:

    def test_if_no_merkzeichen_or_pflegegrad_set_then_return_correct_value_for_disability_degree(self):
        input_output_pairs = [
            (20, None),
            (25, None),
            (30, None),
            (35, None),
            (40, None),
            (45, None),
            (50, None),
            (55, None),
            (60, None),
            (65, None),
            (70, None),
            (75, None),
            (80, 900),
            (85, 900),
            (90, 900),
            (95, 900),
            (100, 900),
        ]

        params = {
            'has_pflegegrad': False,
            'has_merkzeichen_bl': False,
            'has_merkzeichen_tbl': False,
            'has_merkzeichen_h': False,
            'has_merkzeichen_ag': False,
            'has_merkzeichen_g': False,
        }

        for disability_degree, expected_result in input_output_pairs:

            calculated_pauschbetrag = calculate_fahrkostenpauschbetrag(**params, disability_degree=disability_degree)

            assert calculated_pauschbetrag == expected_result

    def test_if_merkzeichen_g_and_no_pflegegrad_set_then_return_correct_value_for_disability_degree(self):
        input_output_pairs = [
            (20, None),
            (30, None),
            (40, None),
            (50, None),
            (60, None),
            (70, 900),
            (80, 900),
            (90, 900),
            (100, 900),
        ]

        params = {
            'has_pflegegrad': False,
            'has_merkzeichen_bl': False,
            'has_merkzeichen_tbl': False,
            'has_merkzeichen_h': False,
            'has_merkzeichen_ag': False,
            'has_merkzeichen_g': True,
        }

        for disability_degree, expected_result in input_output_pairs:

            calculated_pauschbetrag = calculate_fahrkostenpauschbetrag(**params, disability_degree=disability_degree)

            assert calculated_pauschbetrag == expected_result

    def test_if_merkzeichen_bl_and_no_pflegegrad_set_then_return_4500_for_all_disability_degrees(self):
        input_output_pairs = [
            (20, 4500),
            (30, 4500),
            (40, 4500),
            (50, 4500),
            (60, 4500),
            (70, 4500),
            (80, 4500),
            (90, 4500),
            (100, 4500),
        ]

        params = {
            'has_pflegegrad': False,
            'has_merkzeichen_bl': True,
            'has_merkzeichen_tbl': False,
            'has_merkzeichen_h': False,
            'has_merkzeichen_ag': False,
            'has_merkzeichen_g': False,
        }

        for disability_degree, expected_result in input_output_pairs:

            calculated_pauschbetrag = calculate_fahrkostenpauschbetrag(**params, disability_degree=disability_degree)

            assert calculated_pauschbetrag == expected_result

    def test_if_merkzeichen_tbl_and_no_pflegegrad_set_then_return_4500_for_all_disability_degrees(self):
        input_output_pairs = [
            (20, 4500),
            (30, 4500),
            (40, 4500),
            (50, 4500),
            (60, 4500),
            (70, 4500),
            (80, 4500),
            (90, 4500),
            (100, 4500),
        ]

        params = {
            'has_pflegegrad': False,
            'has_merkzeichen_bl': False,
            'has_merkzeichen_tbl': True,
            'has_merkzeichen_h': False,
            'has_merkzeichen_ag': False,
            'has_merkzeichen_g': False,
        }

        for disability_degree, expected_result in input_output_pairs:

            calculated_pauschbetrag = calculate_fahrkostenpauschbetrag(**params, disability_degree=disability_degree)

            assert calculated_pauschbetrag == expected_result

    def test_if_merkzeichen_h_and_no_pflegegrad_set_then_return_4500_for_all_disability_degrees(self):
        input_output_pairs = [
            (20, 4500),
            (30, 4500),
            (40, 4500),
            (50, 4500),
            (60, 4500),
            (70, 4500),
            (80, 4500),
            (90, 4500),
            (100, 4500),
        ]

        params = {
            'has_pflegegrad': False,
            'has_merkzeichen_bl': False,
            'has_merkzeichen_tbl': False,
            'has_merkzeichen_h': True,
            'has_merkzeichen_ag': False,
            'has_merkzeichen_g': False,
        }

        for disability_degree, expected_result in input_output_pairs:

            calculated_pauschbetrag = calculate_fahrkostenpauschbetrag(**params, disability_degree=disability_degree)

            assert calculated_pauschbetrag == expected_result

    def test_if_merkzeichen_ag_and_no_pflegegrad_set_then_return_4500_for_all_disability_degrees(self):
        input_output_pairs = [
            (20, 4500),
            (30, 4500),
            (40, 4500),
            (50, 4500),
            (60, 4500),
            (70, 4500),
            (80, 4500),
            (90, 4500),
            (100, 4500),
        ]

        params = {
            'has_pflegegrad': False,
            'has_merkzeichen_bl': False,
            'has_merkzeichen_tbl': False,
            'has_merkzeichen_h': False,
            'has_merkzeichen_ag': True,
            'has_merkzeichen_g': False,
        }

        for disability_degree, expected_result in input_output_pairs:

            calculated_pauschbetrag = calculate_fahrkostenpauschbetrag(**params, disability_degree=disability_degree)

            assert calculated_pauschbetrag == expected_result

    def test_if_pflegrad_set_and_no_merkzeichen_set_then_return_4500_for_all_disability_degrees(self):
        input_output_pairs = [
            (20, 4500),
            (30, 4500),
            (40, 4500),
            (50, 4500),
            (60, 4500),
            (70, 4500),
            (80, 4500),
            (90, 4500),
            (100, 4500),
        ]

        params = {
            'has_pflegegrad': True,
            'has_merkzeichen_bl': False,
            'has_merkzeichen_tbl': False,
            'has_merkzeichen_h': False,
            'has_merkzeichen_ag': False,
            'has_merkzeichen_g': False,
        }

        for disability_degree, expected_result in input_output_pairs:

            calculated_pauschbetrag = calculate_fahrkostenpauschbetrag(**params, disability_degree=disability_degree)

            assert calculated_pauschbetrag == expected_result

    def test_if_pflegrad_set_and_merkzeichen_bl_set_then_return_4500_for_all_disability_degrees(self):
        input_output_pairs = [
            (20, 4500),
            (30, 4500),
            (40, 4500),
            (50, 4500),
            (60, 4500),
            (70, 4500),
            (80, 4500),
            (90, 4500),
            (100, 4500),
        ]

        params = {
            'has_pflegegrad': True,
            'has_merkzeichen_bl': True,
            'has_merkzeichen_tbl': False,
            'has_merkzeichen_h': False,
            'has_merkzeichen_ag': False,
            'has_merkzeichen_g': False,
        }

        for disability_degree, expected_result in input_output_pairs:

            calculated_pauschbetrag = calculate_fahrkostenpauschbetrag(**params, disability_degree=disability_degree)

            assert calculated_pauschbetrag == expected_result

    def test_if_pflegrad_set_and_merkzeichen_tbl_set_then_return_4500_for_all_disability_degrees(self):
        input_output_pairs = [
            (20, 4500),
            (30, 4500),
            (40, 4500),
            (50, 4500),
            (60, 4500),
            (70, 4500),
            (80, 4500),
            (90, 4500),
            (100, 4500),
        ]

        params = {
            'has_pflegegrad': True,
            'has_merkzeichen_bl': False,
            'has_merkzeichen_tbl': True,
            'has_merkzeichen_h': False,
            'has_merkzeichen_ag': False,
            'has_merkzeichen_g': False,
        }

        for disability_degree, expected_result in input_output_pairs:

            calculated_pauschbetrag = calculate_fahrkostenpauschbetrag(**params, disability_degree=disability_degree)

            assert calculated_pauschbetrag == expected_result

    def test_if_pflegrad_set_and_merkzeichen_h_set_then_return_4500_for_all_disability_degrees(self):
        input_output_pairs = [
            (20, 4500),
            (30, 4500),
            (40, 4500),
            (50, 4500),
            (60, 4500),
            (70, 4500),
            (80, 4500),
            (90, 4500),
            (100, 4500),
        ]

        params = {
            'has_pflegegrad': True,
            'has_merkzeichen_bl': False,
            'has_merkzeichen_tbl': False,
            'has_merkzeichen_h': True,
            'has_merkzeichen_ag': False,
            'has_merkzeichen_g': False,
        }

        for disability_degree, expected_result in input_output_pairs:

            calculated_pauschbetrag = calculate_fahrkostenpauschbetrag(**params, disability_degree=disability_degree)

            assert calculated_pauschbetrag == expected_result

    def test_if_pflegrad_set_and_merkzeichen_ag_set_then_return_4500_for_all_disability_degrees(self):
        input_output_pairs = [
            (20, 4500),
            (30, 4500),
            (40, 4500),
            (50, 4500),
            (60, 4500),
            (70, 4500),
            (80, 4500),
            (90, 4500),
            (100, 4500),
        ]

        params = {
            'has_pflegegrad': True,
            'has_merkzeichen_bl': False,
            'has_merkzeichen_tbl': False,
            'has_merkzeichen_h': False,
            'has_merkzeichen_ag': True,
            'has_merkzeichen_g': False,
        }

        for disability_degree, expected_result in input_output_pairs:

            calculated_pauschbetrag = calculate_fahrkostenpauschbetrag(**params, disability_degree=disability_degree)

            assert calculated_pauschbetrag == expected_result

    def test_if_pflegrad_set_and_merkzeichen_g_set_then_return_4500_for_all_disability_degrees(self):
        input_output_pairs = [
            (20, 4500),
            (30, 4500),
            (40, 4500),
            (50, 4500),
            (60, 4500),
            (70, 4500),
            (80, 4500),
            (90, 4500),
            (100, 4500),
        ]

        params = {
            'has_pflegegrad': True,
            'has_merkzeichen_bl': False,
            'has_merkzeichen_tbl': False,
            'has_merkzeichen_h': False,
            'has_merkzeichen_ag': False,
            'has_merkzeichen_g': True,
        }

        for disability_degree, expected_result in input_output_pairs:

            calculated_pauschbetrag = calculate_fahrkostenpauschbetrag(**params, disability_degree=disability_degree)

            assert calculated_pauschbetrag == expected_result