"""prosper_version.py: utilities to help parse current version information

Props to ccpgames/setuputils for framework

"""
from codecs import decode
import os
from subprocess import check_output
import warnings

import semantic_version

import prosper.common.exceptions as exceptions

DEFAULT_VERSION = '0.0.0'
DEFAULT_BRANCH = 'master'
TEST_MODE = False

def get_version(
        default_version=DEFAULT_VERSION,
        default_branch=DEFAULT_BRANCH
):
    """tries to resolve version number

    Args:
        default_version (str, optional): what version to return if all else fails
        default_branch (str, optional): production branch name

    Returns:
        (str): semantic_version information for library

    """
    if os.environ.get('TRAVIS_TAG'):
        #Running on Travis-CI: trumps all
        if not TEST_MODE:   #pragma: no cover
            return os.environ.get('TRAVIS_TAG').replace('v', '')
        else:
            warnings.warn(
                'Travis detected, but TEST_MODE enabled',
                exceptions.ProsperVersionTestModeWarning)

    current_tag = _read_git_tags(default_version=default_version)

    feature_branch = decode(
        check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]),
        'utf-8').strip()

    current_version = semantic_version.Version(current_tag)
    if feature_branch != default_branch:    #pragma: no cover
        ## Dev mode ##
        warnings.warn(
            'Tagging non-production build',
            exceptions.ProsperNonProductionVersionWarning
        )
        current_version.build = (feature_branch,)

    #TODO: if #steps from tag root, increment minor

    return str(current_version)

def _read_git_tags(
        default_version=DEFAULT_VERSION,
        git_command=['git', 'tag']
):
    """tries to find current git tag

    Notes:
        git_command exposed for testing null case

    Args:
        default_version (str, optional): what version to make
        git_command (:obj:`list`, optional): subprocess command

    Retruns:
        (str): latest version found, or default

    Raises:
        (:obj:`exceptions.ProsperDefaultVersionWarning`): git version not found

    """
    current_tags = check_output(git_command).splitlines()

    if not current_tags:
        warnings.warn(
            'Unable to resolve current version',
            exceptions.ProsperDefaultVersionWarning)
        return default_version

    latest_version = semantic_version.Version(default_version)
    for tag in current_tags:
        tag_str = decode(tag, 'utf-8').replace('v', '')
        try:
            tag_ver = semantic_version.Version(tag_str)
        except Exception:   #pragma: no cover
            continue    #invalid tags ok, but no release

        if tag_ver > latest_version:
            latest_version = tag_ver

    return str(latest_version)
