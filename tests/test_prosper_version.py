"""test_prosper_version.py

Pytest functions for exercising prosper.common.prosper_version

"""
from codecs import decode
from os import path
import os
import shutil
import sys
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

def release_helper():
    """travis is kinda a jerk.  Let's make sure the expected environment is set up"""
    travis_tag = os.environ.get('TRAVIS_TAG')

    if not travis_tag:
        return
    else:
        travis_tag.replace('v', '')
    print('--TRAVIS RELEASE HELPER--')
    print('setting up {} with {}'.format(VERSION_FILEPATH, travis_tag))
    with open(VERSION_FILEPATH, 'w') as v_fh:
        v_fh.write(travis_tag)

release_helper()

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
    version_from_file = version_from_file.replace('v', '')

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

    tag_version = semantic_version.Version(p_version._read_git_tags())
    if tag_version.prerelease:
        pytest.xfail('PyPI prerelease formatting not compatable with `semantic_version`')

    released_versions_report = check_output(['yolk', '-V', 'prospercommon']).splitlines()

    released_versions = []
    for line in released_versions_report:
        released_versions.append(decode(line, 'utf-8').split(' ')[1])

    current_version = max([semantic_version.Version(line) for line in released_versions])


    tag_status = tag_version <= current_version   #expect equal-to or less-than current release

    if os.environ.get('TRAVIS_TAG') and not tag_status:
        pytest.xfail(
            'Drafting release -- tag={} current={}'.format(tag_version, current_version))
    if not tag_status:
        #yolk is flaky
        pytest.xfail(
            'Expected release mismatch -- tag={} yolk={}'.format(tag_version, current_version))
        #assert tag_version <= current_version   #expect equal-to or less-than current release

def test_version_from_file_default():
    """validate default version returns from _version_from_file()"""
    with pytest.warns(exceptions.ProsperDefaultVersionWarning):
        bad_version = p_version._version_from_file(HERE)

    assert bad_version == p_version.DEFAULT_VERSION

def test_version_from_file_happypath():
    """validate version matches expectation"""
    #TODO: meaningless test?
    version_from_file = p_version._version_from_file(PROJECT_HERE_PATH)
    version_from_file = version_from_file.replace('v', '')
    assert version_from_file == version.__version__

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

def test_version_installed_as_dep():
    """validate expected return when installed as dependency"""
    # Prep a dummy version
    virtualenv_name = 'DUMMY_VENV'
    dummy_version = '9.9.9'
    python_version = 'python{major}.{minor}'.format(
        major=sys.version_info[0],
        minor=sys.version_info[1]
    )
    virtualenv_path = path.join(
        HERE, virtualenv_name, 'lib', python_version, 'site-packages/prosper/common')
    os.makedirs(virtualenv_path, exist_ok=True)
    with open(path.join(virtualenv_path, 'version.txt'), 'w') as dummy_fh:
        dummy_fh.write(dummy_version)


    # Test the thing
    assert p_version.get_version(virtualenv_path) == dummy_version

    # Clean up yer mess
    shutil.rmtree(path.join(HERE, virtualenv_name))
