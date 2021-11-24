import pytest
from werkzeug.exceptions import NotFound

from app.utils import non_production_environment_required
from tests.utils import production_flask_env, staging_flask_env


class TestNonProductionEnvironmentRequired:

    @pytest.mark.usefixtures("production_flask_env")
    def test_if_production_environment_set_then_do_return_nop_function(self):
        @non_production_environment_required
        def mock_route_function():
            return "OK", 200

        result = mock_route_function()
        assert result is None

    @pytest.mark.usefixtures("staging_flask_env")
    def test_if_not_production_environment_set_then_do_return_function(self):
        @non_production_environment_required
        def mock_route_function():
            return "OK", 200

        result = mock_route_function()
        assert result == ('OK', 200)
