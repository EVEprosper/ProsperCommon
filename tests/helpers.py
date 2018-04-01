"""TEMPORARY: ported config helpers to ProsperTestHelpers"""
import configparser
from os import path
from datetime import datetime
import warnings

import prosper.common.prosper_config as p_config

def get_config(
        config_filepath,
        local_override=False
):
    """DEPRECATED: classic v1 config parser.  Obsolete by v0.3.0"""
    warnings.warn(
        __name__ + 'replaced with ProsperConfig',
        DeprecationWarning
    )
    config = configparser.ConfigParser(
        interpolation=configparser.ExtendedInterpolation(),
        allow_no_value=True,
        delimiters=('='),
        inline_comment_prefixes=('#')
    )

    real_config_filepath = p_config.get_local_config_filepath(config_filepath)

    if local_override:  #force lookup tracked config
        real_config_filepath = config_filepath

    with open(real_config_filepath, 'r') as filehandle:
        config.read_file(filehandle)
    return config

def compare_config_files(config_filepath):
    """compares prod config file vs local version

    Args:
        config_filepath (str): path to config file

    Returns:
        dict: description of unique keys between both configs

    """
    tracked_config = get_config(config_filepath, True)
    local_config = get_config(config_filepath)

    unique_values = {}

    if not path.isfile(p_config.get_local_config_filepath(config_filepath)): #pragma: no cover
        #pytest.skip('no local .cfg found, skipping')
        return None

    local_unique_sections, local_unique_keys = find_unique_keys(
        local_config,
        tracked_config,
        'local'
    )
    tracked_unique_sections, tracked_unique_keys = find_unique_keys(
        tracked_config,
        local_config,
        'tracked'
    )

    ## vv TODO vv: TEST ME ##
    if any([
            local_unique_keys,
            tracked_unique_keys
    ]):
        unique_values['unique_keys'] = {}
        unique_values['unique_keys']['local'] = local_unique_keys
        unique_values['unique_keys']['tracked'] = tracked_unique_keys
    if any([
            local_unique_sections,
            tracked_unique_sections
    ]):
        unique_values['unique_sections'] = [local_unique_sections, tracked_unique_sections]
    ## ^^ TODO ^^ ##

    return unique_values

def find_unique_keys(base_config, comp_config, base_name):
    """walks through base_config and looks for keys missing in comp_config

    Args:
        base_config (:obj:`configparser.ConfigParser`): BASE config for comparison
        comp_config (:obj:`configparser.ConfigParser`): COMP config for comparison
        base_name (str): name to tag mismatches with

    Returns:
        list: unique sections from ConfigParser
        list: unique keys from ConfigParser sections

    """
    unique_keys = []
    unique_sections = []

    for section in base_config:
        if str(section) == 'DEFAULT':
            continue #.cfg has DEFAULT key, we do not use
        if not comp_config.has_section(section):
            unique_label = base_name + '.' + str(section)
            unique_sections.append(unique_label)
            continue

        for key in base_config[section]:
            if not comp_config.has_option(section, key):
                unique_label = str(section) + '.' + str(key)
                unique_keys.append(unique_label)
                continue
            #TODO: compare values?
    return unique_sections, unique_keys
