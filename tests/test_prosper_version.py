"""test_prosper_version.py

Pytest functions for exercising prosper.common.prosper_version

"""
from codecs import decode
from os import path
import os
from subprocess import check_output

import pytest
import semantic_version

import prosper.common.prosper_version as p_version
import prosper.common._version as version
import prosper.common.exceptions as exceptions

HERE = path.abspath(path.dirname(__file__))
ROOT = path.dirname(HERE)

PROJECT_HERE_PATH = path.join(ROOT, 'prosper', 'common')
VERSION_FILEPATH = path.join(PROJECT_HERE_PATH, 'version.txt')

if os.environ.get('TRAVIS_TAG'):
    p_version.get_version(PROJECT_HERE_PATH) #init for TRAVIS

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

    assert version_from_file == p_version.get_version(PROJECT_HERE_PATH)

def test_read_git_tags_default():
    """validate default version returns from _read_git_tags()"""
    null_command = ['echo']

    with pytest.warns(exceptions.ProsperDefaultVersionWarning):
        no_version = p_version._read_git_tags(git_command=null_command)

    assert no_version == p_version.DEFAULT_VERSION

def test_read_git_tags_happypath():
    """validate version matches expectation"""

    released_versions_report = check_output(['yolk', '-V', 'prospercommon']).splitlines()

    released_versions = []
    for line in released_versions_report:
        released_versions.append(decode(line, 'utf-8').split(' ')[1])

    current_version = max([semantic_version.Version(line) for line in released_versions])

    tag_version = semantic_version.Version(p_version._read_git_tags())

    tag_status = tag_version <= current_version   #expect equal-to or less-than current release

    if os.environ.get('TRAVIS_TAG') and not tag_status:
        pytest.xfail(
            'Drafting release -- tag={} current={}'.format(tag_version, current_version))

    assert tag_version <= current_version   #expect equal-to or less-than current release
def test_version_from_file_default():
    """validate default version returns from _version_from_file()"""
    with pytest.warns(exceptions.ProsperDefaultVersionWarning):
        bad_version = p_version._version_from_file(HERE)

    assert bad_version == p_version.DEFAULT_VERSION

def test_version_from_file_happypath():
    """validate version matches expectation"""
    #TODO: meaningless test?
    assert p_version._version_from_file(PROJECT_HERE_PATH) == version.__version__

def test_travis_tag_testmode():
    """validate testmode can reach expected path"""
    old_environ = os.environ.get('TRAVIS_TAG')
    p_version.TEST_MODE = True
    if not old_environ:
        os.environ['TRAVIS_TAG'] = 'DUMMY'

    with pytest.warns(exceptions.ProsperVersionTestModeWarning):
        travis_version = p_version.get_version(PROJECT_HERE_PATH)

    assert travis_version == version.__version__

    ## return environ to as expected
    p_version.TEST_MODE = False
    if old_environ:
        os.environ['TRAVIS_TAG'] = old_environ
