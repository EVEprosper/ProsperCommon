"""test_flask_utils: validates expected behavior for prosper.common.flask_utils"""
import atexit
import importlib.util
from os import path, environ, remove
import platform

import pytest
from plumbum import local

import prosper.common.flask_utils as flask_utils

HERE = path.abspath(path.dirname(__file__))
ROOT = path.dirname(HERE)

python = local['python']
if platform.system() == 'Windows':
    which = local['where']
else:
    which = local['which']


def test_cli():
    """make sure entry_point/console_script does what it says"""
    # TODO: local.cwd() swapping to test dirs
    gunicorn_conf = local[which('make_gunicorn_config').rstrip()]
    if path.isfile('gunicorn.conf'):
        remove('gunicorn.conf')

    gunicorn_conf()

    assert path.isfile('gunicorn.conf')

def test_gunicorn_conf():
    """make sure gunicorn contents works as expected"""
    # Prep Test
    environ['GUNICORN_TEST1'] = 'hello'
    environ['GUNICORN_TEST2'] = 'world'
    gunicorn_filename = path.join(HERE, '_gunicorn.py')
    if path.isfile(gunicorn_filename):
        remove(gunicorn_filename)

    # Create gunicorn config file (.py)
    flask_utils.make_gunicorn_config(_gunicorn_config_path=gunicorn_filename)
    assert path.isfile(gunicorn_filename)

    # use importlib to load _gunicorn.py and make sure expected values are there
    spec = importlib.util.spec_from_file_location('_gunicorn', gunicorn_filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    assert module.test1 == 'hello'
    assert module.test2 == 'world'
