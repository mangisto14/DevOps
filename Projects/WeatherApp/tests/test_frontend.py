"""
Frontend unit tests - verifies the Flask frontend app renders correctly
and passes the backend URL to the template.
"""
import os
import pytest


class TestFrontendHealthEndpoint:
    def test_health_returns_200(self, frontend_client):
        res = frontend_client.get('/health')
        assert res.status_code == 200

    def test_health_returns_healthy_status(self, frontend_client):
        data = frontend_client.get('/health').get_json()
        assert data['status'] == 'healthy'


class TestFrontendIndex:
    def test_index_returns_200(self, frontend_client):
        res = frontend_client.get('/')
        assert res.status_code == 200

    def test_index_contains_backend_url_in_html(self, frontend_client):
        from conftest import frontend_module
        res = frontend_client.get('/')
        html = res.data.decode('utf-8')
        assert frontend_module.BACKEND_URL in html

    def test_index_contains_city_select(self, frontend_client):
        html = frontend_client.get('/').data.decode('utf-8')
        assert 'city-select' in html

    def test_index_contains_all_city_options(self, frontend_client):
        html = frontend_client.get('/').data.decode('utf-8')
        for city in ('newyork', 'sydney', 'capetown', 'bangkok'):
            assert f'value="{city}"' in html, f"City option missing: {city}"

    def test_index_contains_get_weather_button(self, frontend_client):
        html = frontend_client.get('/').data.decode('utf-8')
        assert 'get-weather-btn' in html

    def test_index_embeds_backend_url_in_data_attribute(self, frontend_client):
        html = frontend_client.get('/').data.decode('utf-8')
        assert 'data-backend-url' in html


class TestFrontendBackendUrlConfig:
    def test_default_backend_url_fallback_is_localhost(self):
        default = os.getenv('BACKEND_URL', 'http://localhost:5000')
        if 'BACKEND_URL' not in os.environ:
            assert 'localhost' in default

    def test_backend_url_env_var_is_read_from_environment(self):
        from conftest import frontend_module
        assert frontend_module.BACKEND_URL == os.getenv('BACKEND_URL', 'http://localhost:5000')
