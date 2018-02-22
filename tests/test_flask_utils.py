"""test_flask_utils: validates expected behavior for prosper.common.flask_utils"""
import atexit
from os import path, environ
import importlib

from plumbum import local

HERE = path.abspath(path.dirname(__file__))

COMMAND_NAME = 'make_gunicorn_config'
GUNICORN_FILE = path.join(HERE, 'gunicorn.config')

FAKE_CONFIGS = {
    'GUNICORN_FAKE1': 10,
    'GUNICORN_FAKE2': 'threadded'
}

for config_key, config_value in FAKE_CONFIGS.items():
    environ[config_key] = config_value
    atexit.register(cleanup_configs, config_key)

def cleanup_configs(config_key):
    """atexit handle that cleans up environ at end-of-test"""
    del environ[config_key]
