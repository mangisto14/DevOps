"""
Backend unit tests - verifies the Flask API returns correct weather data structure.
Uses mocking to avoid real OpenWeatherMap API calls.
"""
import pytest
from unittest.mock import patch, MagicMock


MOCK_OWM_RESPONSE = {
    "name": "New York",
    "main": {"temp": 22.5, "humidity": 65},
    "weather": [{"description": "clear sky"}],
    "wind": {"speed": 3.2}
}


class TestHealthEndpoint:
    def test_health_returns_200(self, backend_client):
        res = backend_client.get('/health')
        assert res.status_code == 200

    def test_health_returns_healthy_status(self, backend_client):
        data = backend_client.get('/health').get_json()
        assert data['status'] == 'healthy'


class TestLocationsEndpoint:
    def test_locations_returns_200(self, backend_client):
        res = backend_client.get('/locations')
        assert res.status_code == 200

    def test_locations_contains_all_cities(self, backend_client):
        data = backend_client.get('/locations').get_json()
        expected = {'newyork', 'sydney', 'capetown', 'bangkok'}
        assert expected == set(data['supported_locations'])

    def test_locations_has_display_names(self, backend_client):
        data = backend_client.get('/locations').get_json()
        assert data['location_names']['newyork'] == 'New York'
        assert data['location_names']['sydney'] == 'Sydney'
        assert data['location_names']['capetown'] == 'Cape Town'
        assert data['location_names']['bangkok'] == 'Bangkok'


class TestWeatherEndpoint:
    @patch('weather_backend.requests.get')
    def test_weather_returns_200_for_valid_city(self, mock_get, backend_client):
        mock_resp = MagicMock()
        mock_resp.json.return_value = MOCK_OWM_RESPONSE
        mock_resp.raise_for_status.return_value = None
        mock_get.return_value = mock_resp

        res = backend_client.get('/weather/newyork')
        assert res.status_code == 200

    @patch('weather_backend.requests.get')
    def test_weather_response_has_required_fields(self, mock_get, backend_client):
        mock_resp = MagicMock()
        mock_resp.json.return_value = MOCK_OWM_RESPONSE
        mock_resp.raise_for_status.return_value = None
        mock_get.return_value = mock_resp

        data = backend_client.get('/weather/newyork').get_json()
        for field in ('city', 'temperature', 'description', 'humidity', 'wind_speed'):
            assert field in data, f"Missing field: {field}"

    @patch('weather_backend.requests.get')
    def test_weather_returns_correct_values(self, mock_get, backend_client):
        mock_resp = MagicMock()
        mock_resp.json.return_value = MOCK_OWM_RESPONSE
        mock_resp.raise_for_status.return_value = None
        mock_get.return_value = mock_resp

        data = backend_client.get('/weather/newyork').get_json()
        assert data['city'] == 'New York'
        assert data['temperature'] == 22.5
        assert data['description'] == 'clear sky'
        assert data['humidity'] == 65
        assert data['wind_speed'] == 3.2

    @patch('weather_backend.requests.get')
    def test_weather_works_for_all_cities(self, mock_get, backend_client):
        mock_resp = MagicMock()
        mock_resp.raise_for_status.return_value = None
        mock_get.return_value = mock_resp

        for city in ('newyork', 'sydney', 'capetown', 'bangkok'):
            mock_resp.json.return_value = {**MOCK_OWM_RESPONSE, "name": city}
            res = backend_client.get(f'/weather/{city}')
            assert res.status_code == 200, f"Failed for city: {city}"

    def test_weather_returns_400_for_invalid_city(self, backend_client):
        res = backend_client.get('/weather/unknowncity')
        assert res.status_code == 400

    def test_weather_invalid_city_returns_error_message(self, backend_client):
        data = backend_client.get('/weather/unknowncity').get_json()
        assert 'error' in data
        assert 'supported_locations' in data

    @patch('weather_backend.requests.get')
    def test_weather_handles_api_timeout(self, mock_get, backend_client):
        import requests as req
        mock_get.side_effect = req.exceptions.Timeout()

        res = backend_client.get('/weather/newyork')
        assert res.status_code == 504

    @patch('weather_backend.requests.get')
    def test_weather_calls_openweathermap_with_correct_city(self, mock_get, backend_client):
        mock_resp = MagicMock()
        mock_resp.json.return_value = MOCK_OWM_RESPONSE
        mock_resp.raise_for_status.return_value = None
        mock_get.return_value = mock_resp

        backend_client.get('/weather/sydney')
        call_kwargs = mock_get.call_args[1]['params']
        assert call_kwargs['q'] == 'Sydney'
        assert call_kwargs['units'] == 'metric'
