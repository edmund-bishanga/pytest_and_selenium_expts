#!/usr/bin/python

"""
Misc Experiments:
+ config file parsing: ini, yml, json
"""

# pylint: disable=missing-function-docstring
# pylint: disable=use-list-literal

# imports: Std, 3rdParty, CustomLocal
import sys
import time
from configparser import ConfigParser
from datetime import date, timedelta
from pprint import pprint

import matplotlib.pyplot as plt
import numpy as np
import pytest
import yaml
from yaml.loader import SafeLoader

from log_modules.log_gardening import LogGardening

DEF_ENCODING = 'utf-8'

def print_file_contents(filepath):
    with open(filepath, 'r', encoding=DEF_ENCODING) as file:
        content = file.read()
    delim = '++++++++++++++++++++'
    print(delim)
    print(content)
    print(delim)

def read_ini_config_file(conf_ini_file):
    config = ConfigParser()
    config.read(conf_ini_file)
    print('Config: Sections: ', config.sections(), '\n')
    for section in config.sections():
        print('Config: section values: {}: {}'.format(
                section, [(val, config.get(section, val)) for val in config.options(section)]
            )
        )
    print('\nConfig: param: str: ', config.get('build', 'library'))
    print('Config: int: ', config.get('operation', 'timeout'))
    print('Config: bool: ', config.get('operation', 'offset'))

def get_yaml_config(conf_yml_file):
    """ reads a YAML config file: ideally with one config """
    config = {}
    with open(conf_yml_file, 'r', encoding=DEF_ENCODING) as file_obj:
        config = yaml.load(file_obj, Loader=SafeLoader)
        pprint(config, width=120)
    assert config, '{}: invalid .yaml config file'.format(conf_yml_file)
    return config

def get_yaml_config_section_kvs(yaml_config, sect_name):
    err_msg = '\n"{}": not in {}'.format(sect_name, yaml_config.keys())
    # assert sect_name in yaml_config.keys(), err_msg
    if sect_name not in yaml_config.keys():
        print(err_msg)
    return yaml_config.get(sect_name)

def main():
    """ Experiment with Config Parsing. """

    # parse .yaml file
    config_yml_file = "./configs/sample_config.yml"
    yml_config = get_yaml_config(config_yml_file)
    print('\nDEBUG: main: yml_config:')
    pprint(yml_config)

    key_names = ['mode', 'logs']
    for sect_name in ['Build', 'Random', None, '', 'Configure']:
        sect_kvs = get_yaml_config_section_kvs(yml_config, sect_name)
        print(f'\nDEBUG: main: {sect_name}: kvs:')
        pprint(sect_kvs)
        if sect_kvs:
            for item in sect_kvs:
                # print(f'\nDEBUG: section: {sect_name}: item: {item}')
                for key in item.keys():
                    if key in key_names:
                        print(f'section: {sect_name}, item: [{key}: "{item.get(key)}"]')

    # parse .ini file
    conf_ini_file = './configs/sample_config.ini'
    print_file_contents(conf_ini_file)
    read_ini_config_file(conf_ini_file)


if __name__ == '__main__':
    main()
