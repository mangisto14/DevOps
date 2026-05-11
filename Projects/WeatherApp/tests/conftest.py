"""
Shared fixtures - loads backend and frontend as uniquely-named modules
to avoid Python's module cache collision (both services are named 'app').
"""
import sys
import os
import importlib.util
import pytest

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def _load_module(unique_name, file_path):
    spec = importlib.util.spec_from_file_location(unique_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[unique_name] = module
    spec.loader.exec_module(module)
    return module


backend_module = _load_module(
    'weather_backend',
    os.path.join(BASE_DIR, 'weather-backend', 'app.py')
)

frontend_module = _load_module(
    'weather_frontend',
    os.path.join(BASE_DIR, 'weather-frontend', 'app.py')
)


@pytest.fixture(scope='session')
def backend_app():
    backend_module.app.config['TESTING'] = True
    return backend_module.app


@pytest.fixture(scope='session')
def frontend_app():
    frontend_module.app.config['TESTING'] = True
    return frontend_module.app


@pytest.fixture
def backend_client(backend_app):
    with backend_app.test_client() as client:
        yield client


@pytest.fixture
def frontend_client(frontend_app):
    with frontend_app.test_client() as client:
        yield client
