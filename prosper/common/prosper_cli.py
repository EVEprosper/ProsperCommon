"""Plumbum CLI wrapper for easier/common application writing"""
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

    config_path = None  # TODO: force child to implement var?
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
    def logger():
        """builds a logger on-demand when first called"""
        pass

    @property
    def config():
        """builds a ProsperConfig object on-demand when first called"""
        pass

if __name__ == '__main__':
    ProsperApplication.run()  # test hook
