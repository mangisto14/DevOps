"""
Integration tests - verifies the full data flow:
  Frontend → Backend → (mocked) OpenWeatherMap API

Verifies that:
1. The backend returns a schema the frontend JavaScript can consume
2. The frontend HTML exposes the backend URL correctly to JavaScript
3. All cities round-trip with correct data types and values
4. Error responses are always JSON so the frontend can handle them
"""
import os
import pytest
from unittest.mock import patch, MagicMock


MOCK_OWM_RESPONSE = {
    "name": "New York",
    "main": {"temp": 18.0, "humidity": 72},
    "weather": [{"description": "light rain"}],
    "wind": {"speed": 5.1}
}

FRONTEND_EXPECTED_KEYS = {'city', 'temperature', 'description', 'humidity', 'wind_speed'}


class TestBackendResponseSchema:
    """Verify the backend returns a schema the frontend JavaScript can consume."""

    @patch('weather_backend.requests.get')
    def test_weather_response_matches_frontend_expected_fields(self, mock_get, backend_client):
        mock_resp = MagicMock()
        mock_resp.json.return_value = MOCK_OWM_RESPONSE
        mock_resp.raise_for_status.return_value = None
        mock_get.return_value = mock_resp

        data = backend_client.get('/weather/newyork').get_json()
        assert FRONTEND_EXPECTED_KEYS == set(data.keys())

    @patch('weather_backend.requests.get')
    def test_temperature_is_numeric(self, mock_get, backend_client):
        mock_resp = MagicMock()
        mock_resp.json.return_value = MOCK_OWM_RESPONSE
        mock_resp.raise_for_status.return_value = None
        mock_get.return_value = mock_resp

        data = backend_client.get('/weather/newyork').get_json()
        assert isinstance(data['temperature'], (int, float))

    @patch('weather_backend.requests.get')
    def test_humidity_is_numeric(self, mock_get, backend_client):
        mock_resp = MagicMock()
        mock_resp.json.return_value = MOCK_OWM_RESPONSE
        mock_resp.raise_for_status.return_value = None
        mock_get.return_value = mock_resp

        data = backend_client.get('/weather/newyork').get_json()
        assert isinstance(data['humidity'], (int, float))

    @patch('weather_backend.requests.get')
    def test_wind_speed_is_numeric(self, mock_get, backend_client):
        mock_resp = MagicMock()
        mock_resp.json.return_value = MOCK_OWM_RESPONSE
        mock_resp.raise_for_status.return_value = None
        mock_get.return_value = mock_resp

        data = backend_client.get('/weather/newyork').get_json()
        assert isinstance(data['wind_speed'], (int, float))

    @patch('weather_backend.requests.get')
    def test_description_is_string(self, mock_get, backend_client):
        mock_resp = MagicMock()
        mock_resp.json.return_value = MOCK_OWM_RESPONSE
        mock_resp.raise_for_status.return_value = None
        mock_get.return_value = mock_resp

        data = backend_client.get('/weather/newyork').get_json()
        assert isinstance(data['description'], str)
        assert len(data['description']) > 0


class TestFrontendBackendCommunication:
    """Verify the frontend is correctly configured to call the backend."""

    def test_frontend_html_exposes_backend_url_to_javascript(self, frontend_client):
        from conftest import frontend_module
        html = frontend_client.get('/').data.decode('utf-8')
        assert frontend_module.BACKEND_URL in html

    def test_frontend_backend_url_is_in_data_attribute(self, frontend_client):
        from conftest import frontend_module
        html = frontend_client.get('/').data.decode('utf-8')
        assert f'data-backend-url="{frontend_module.BACKEND_URL}"' in html

    def test_frontend_javascript_file_constructs_weather_url(self):
        js_path = os.path.join(
            os.path.dirname(__file__), '..', 'weather-frontend', 'static', 'script.js'
        )
        with open(js_path) as f:
            js = f.read()
        assert '`${BACKEND_URL}/weather/${selectedCity}`' in js

    def test_frontend_javascript_parses_all_required_fields(self):
        js_path = os.path.join(
            os.path.dirname(__file__), '..', 'weather-frontend', 'static', 'script.js'
        )
        with open(js_path) as f:
            js = f.read()
        for field in ('city', 'temperature', 'description', 'humidity', 'wind_speed'):
            assert f"data.{field}" in js, f"JavaScript does not read field: {field}"


class TestDataFlowEndToEnd:
    """Verifies each city's data round-trips correctly end-to-end."""

    @patch('weather_backend.requests.get')
    @pytest.mark.parametrize("city_key,city_name", [
        ("newyork", "New York"),
        ("sydney", "Sydney"),
        ("capetown", "Cape Town"),
        ("bangkok", "Bangkok"),
    ])
    def test_all_cities_return_valid_data(self, mock_get, city_key, city_name, backend_client):
        owm_response = {
            "name": city_name,
            "main": {"temp": 25.0, "humidity": 60},
            "weather": [{"description": "sunny"}],
            "wind": {"speed": 4.0}
        }
        mock_resp = MagicMock()
        mock_resp.json.return_value = owm_response
        mock_resp.raise_for_status.return_value = None
        mock_get.return_value = mock_resp

        res = backend_client.get(f'/weather/{city_key}')
        assert res.status_code == 200
        data = res.get_json()
        assert data['city'] == city_name
        assert data['temperature'] == 25.0
        assert data['humidity'] == 60
        assert data['wind_speed'] == 4.0
        assert data['description'] == 'sunny'

    @patch('weather_backend.requests.get')
    def test_backend_error_response_is_json(self, mock_get, backend_client):
        """Frontend error handler expects JSON; verify backend always returns JSON on timeout."""
        import requests as req
        mock_get.side_effect = req.exceptions.Timeout()

        res = backend_client.get('/weather/newyork')
        assert res.status_code == 504
        assert res.content_type == 'application/json'
        data = res.get_json()
        assert 'error' in data

    def test_invalid_city_error_response_is_json(self, backend_client):
        """Frontend error handler expects JSON for 400 responses too."""
        res = backend_client.get('/weather/invalidcity')
        assert res.status_code == 400
        assert res.content_type == 'application/json'
        data = res.get_json()
        assert 'error' in data
