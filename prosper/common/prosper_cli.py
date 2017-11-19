"""Plumbum CLI wrapper for easier/common application writing"""
import abc
import platform

from plumbum import cli

import prosper.common.prosper_logging as p_logging


class ProsperApplication(cli.Application):
    """parent-wrapper for CLI applications"""

    debug = cli.Flag(
        ['d', '--debug'],
        help='DEBUG MODE: do not write to prod'
    )

    verbose = cli.Flag(
        ['v', '--verbose'],
        help='enable verbose messaging'
    )

    def __new__(cls, *args, **kwargs):
        """wrapper for ensuring expected functions"""
        if not hasattr(cls, 'config_path'):
            raise NotImplementedError(
                '`config_path` required path to default .cfg file'
            )
        return super(cli.Application, cls).__new__(cls)  # don't break cli.Application

    @cli.switch(
        ['--config'],
        str,
        help='Override default config')
    def override_config(self, config_path):
        """override config object with local version"""
        self.config_path = config_path

    @cli.switch(
        ['--dump-config'],
        help='Dump default config to stdout')
    def dump_config(self):
        """dumps configfile to stdout so users can edit/implement their own"""
        with open(self.config_path, 'r') as cfg_fh:
            base_config = cfg_fh.read()

        print(base_config)
        exit()

    @property
    def logger(self):
        """builds a logger on-demand when first called"""
        pass

    @property
    def config(self):
        """builds a ProsperConfig object on-demand when first called"""
        pass


class ProsperTESTApplication(ProsperApplication):
    """test wrapper for CLI tests"""
    from os import path
    PROGNAME = 'CLITEST'
    VERSION = '0.0.0'

    HERE = path.abspath(path.dirname(__file__))

    config_path = path.join(HERE, 'common_config.cfg')

    def main(self):
        """do stuff"""
        print('hello world')

if __name__ == '__main__':
    ProsperTESTApplication.run()  # test hook
