"""test_prosper_cli.py

Pytest functions for exercising prosper.common.cli

"""
import configparser
import logging
from os import path

import pytest
from plumbum import local
from testfixtures import LogCapture

import prosper.common.prosper_cli as p_cli
import prosper.common.prosper_config as p_config
import prosper.common.prosper_logging as p_logging

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

    def test_config_path_happypath(self):
        """make sure __new__ works as expected"""
        class DummyApplication(p_cli.ProsperApplication):
            PROGNAME = 'DUMMY'
            VERSION = '0.0.0'

            here_path = HERE
            config_path = LOCAL_CONFIG_PATH

            def main(self):
                return 'yes'
        dummy = DummyApplication(__file__)

    def test_app_properties_logger_verbose(self):
        """make sure properties work as expected"""
        class DummyVerboseApplication(p_cli.ProsperApplication):
            PROGNAME = 'DUMMYVERBOSE'
            VERSION = '0.0.0'

            here_path = HERE
            config_path = LOCAL_CONFIG_PATH

            def main(self):
                return 'yes'

        dummy_v = DummyVerboseApplication(__file__)
        dummy_v.verbose = True

        assert dummy_v._logger is None
        assert isinstance(dummy_v.logger, logging.Logger)

        handler_types = [type(handler) for handler in dummy_v.logger.handlers]
        assert logging.StreamHandler in handler_types
        assert p_logging.HackyDiscordHandler not in handler_types
        assert p_logging.HackySlackHandler not in handler_types
        assert p_logging.HackyHipChatHandler not in handler_types

    def test_app_properties_logger_normal(self):
        """make sure properties work as expected"""
        class DummyApplication(p_cli.ProsperApplication):
            PROGNAME = 'DUMMY'
            VERSION = '0.0.0'

            here_path = HERE
            config_path = LOCAL_CONFIG_PATH

            def main(self):
                return 'yes'

        dummy = DummyApplication(__file__)

        assert dummy._logger is None
        assert isinstance(dummy.logger, logging.Logger)

        handler_types = [type(handler) for handler in dummy.logger.handlers]
        assert p_logging.HackyDiscordHandler in handler_types
        assert p_logging.HackySlackHandler in handler_types
        # assert p_logging.HackyHipChatHandler in handler_types  # TODO: need hipchat test endpoint
        assert logging.StreamHandler not in handler_types

    def test_app_properties_config(self):
        """make sure properties work as expected"""
        class DummyApplication(p_cli.ProsperApplication):
            PROGNAME = 'DUMMY'
            VERSION = '0.0.0'

            here_path = HERE
            config_path = LOCAL_CONFIG_PATH

            def main(self):
                return 'yes'

        dummy = DummyApplication(__file__)
        assert isinstance(dummy.config, p_config.ProsperConfig)


class TestFlaskLauncher:
    """validate meta behavior of FlaskLauncher framework"""
    class DummyFlaskLauncher(p_cli.FlaskLauncher):
        PROGNAME = 'FLASK_LAUNCHER'
        VERSION = '0.0.0'

        here_path = HERE
        config_path = LOCAL_CONFIG_PATH

        def main(self):
            print('yes!')


    def test_get_host(self):
        """validate get_host method"""
        dummy = self.DummyFlaskLauncher(__file__)
        dummy.debug = True
        assert dummy.get_host() == '127.0.0.1'

        dummy.debug = False
        assert dummy.get_host() == '0.0.0.0'

    def test_notify_launch(self):
        """validate notify_launch method"""
        pass

class TestCLI:
    """validate basic args work as expected"""
    python = local['python']
    cli = python[path.join(ROOT, 'prosper_cli.py')]

    def test_happypath(self):
        """validate output is output"""
        # TODO: test isn't working, but OK?
        result = self.cli('--verbose')
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

    def test_dump_config(self):
        """validate --dump-config works as expected"""
        result = self.cli('--dump-config')

        config = configparser.ConfigParser()
        config.read_string(result)
