"""prosper_version.py: utilities to help parse current version information

Props to ccpgames/setuputils for framework

"""
from codecs import decode
import os
from subprocess import check_output
import warnings

import semantic_version

def get_version():
    """tries to resolve version number

    Returns:
        (str): semantic_version information for library

    """
    pass
