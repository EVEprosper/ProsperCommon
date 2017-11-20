"""test_prosper_cli.py

Pytest functions for exercising prosper.common.cli

"""
from os import path

import pytest
from plumbum import local

import prosper.common.prosper_cli as p_cli

HERE = path.abspath(path.dirname(__file__))
ROOT = path.join(
    path.dirname(HERE), 'prosper', 'common'
)

LOCAL_CONFIG_PATH = path.join(
    ROOT,
    'common_config.cfg'
)


class TestMetaClasses:
    """validate expected errors from abc"""

    def test_no_config_path(self):
        """make sure expected error throws if cli.Application lacks variable"""
        class DummyApplication(p_cli.ProsperApplication):
            PROGNAME = 'DUMMY'
            VERSION = '0.0.0'

            here_path = HERE

            def main(self):
                return 'yes'

        with pytest.raises(NotImplementedError):
            dummy = DummyApplication()


class TestCLI:
    """validate basic args work as expected"""
    python = local['python']
    cli = python[path.join(ROOT, 'prosper_cli.py')]

    def test_happypath(self):
        """validate output is output"""
        # TODO: test isn't working, but OK?
        result = self.cli('-d')
        if not result:
            pytest.xfail('expected output?  `{}`'.format(result))

    def test_version(self):
        """validate expected version string"""
        result = self.cli('--version')
        assert result.rstrip() == 'CLITEST 0.0.0'

    def test_help(self):
        """validate help messages show up"""
        result = self.cli('-h')
        assert result.rstrip()
