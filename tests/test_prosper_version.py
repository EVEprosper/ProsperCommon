"""test_prosper_version.py

Pytest functions for exercising prosper.common.prosper_version

"""
from os import path

import pytest
import semantic_version

import prosper.common.prosper_version as prosper_version
import prosper.common._version as version
import prosper.common.exceptions as exceptions

HERE = path.abspath(path.dirname(__file__))
ROOT = path.dirname(HERE)

PROJECT_HERE_PATH = path.join(ROOT, 'prosper', 'common')
VERSION_FILEPATH = path.join(PROJECT_HERE_PATH, 'version.txt')

def test_version_virgin():
    """validate first-install overrides"""
    version.INSTALLED = False

    with pytest.warns(UserWarning):
        default_version = version.get_version()

    assert default_version == '0.0.0'
    assert semantic_version.Version(default_version)

    assert version.__version__ != default_version

    #reset default
    version.INSTALLED = True

def test_version_expected():
    """validate __version__ meets expectations"""
    #TODO: meaningless test?
    with open(VERSION_FILEPATH, 'r') as v_fh:
        version_from_file = v_fh.read()

    assert version_from_file == version.__version__

    assert version_from_file == prosper_version.get_version(PROJECT_HERE_PATH)
