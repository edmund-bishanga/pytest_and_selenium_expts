#!usr/bin/python

"""
Misc Experiments:
+ log file processing
+ pytest, etc
"""
# pylint: disable=missing-function-docstring

import sys
# imports: Std, 3rdParty, CustomLocal
import time
from configparser import ConfigParser
from datetime import date, timedelta
from pprint import pprint

import matplotlib.pyplot as plt
import numpy as np
import pytest
import yaml
from yaml.loader import SafeLoader


def sum_to_n(num=1):
    total = 0
    for numero in range(1, num+1):
        total = total + numero
    return total

t_inputs = [(1, 1), (2, 3), (3, 6), (4, 10), (5, 15), (10, 55), (100, 5050)]
@pytest.mark.parametrize("n_input, exp_output", t_inputs)
def test_sum_to_n(n_input, exp_output):
    actual_result = sum_to_n(n_input)
    err_msg = 'input: {}: unexpected result'.format(n_input)
    assert actual_result == exp_output, err_msg

def print_file_contents(filepath):
    with open(filepath, 'r') as file:
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
    with open(conf_yml_file, 'r') as file_obj:
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

def convert_epoch_to_datetime(epoch_time):
    t_format = '%Y-%m-%d %H:%M:%S'
    t_format = '%a/%d.%b.%Y %H:%M:%S'
    return time.strftime(t_format, time.localtime(epoch_time))

def get_time_str_n_weeks_away(n_weeks, start_date_str=None):
    # start date
    start_date = date.today() if not start_date_str else date.fromisoformat(start_date_str)
    print('DEBUG: start_date: ', start_date)
    # calculate date n weeks forward
    print('DEBUG: n_weeks: ', n_weeks)
    n_wks_date = start_date + timedelta(weeks=n_weeks)
    return n_wks_date

def plot_2d_cartesian(x_list, y_list, title=None, xlabel=None, ylabel=None, figwidth=10, figheight=4, out_path=None):
    fig = plt.figure()
    fig.set_figwidth(figwidth)
    fig.set_figheight(figheight)
    plt.title(title if title else '')
    plt.xlabel(xlabel if xlabel else '')
    plt.ylabel(ylabel if ylabel else '')
    plt.plot(x_list, y_list)
    plt.savefig(out_path) if out_path else plt.show()

def main():
    """ Misc Experiments, testing modules """

    # parse .yaml file
    config_yml_file = "./configs/sample_config.yml"
    yml_config = get_yaml_config(config_yml_file)
    print('\nDEBUG: main: yml_config:'); pprint(yml_config)

    key_names = ['mode', 'logs']
    for sect_name in ['Build', 'Random', None, '', 'Configure']:
        sect_kvs = get_yaml_config_section_kvs(yml_config, sect_name)
        print('\nDEBUG: main: {}: kvs:'.format(sect_name)); pprint(sect_kvs)
        if sect_kvs:
            for item in sect_kvs:
                # print('\nDEBUG: section: {}: item: {}'.format(sect_name, item))
                for key in item.keys():
                    if key in key_names:
                        print('section: {}, item: [{}: "{}"]'.format(sect_name, key, item.get(key)))

    # default_NTDD = get_time_str_n_weeks_away(10)
    # print('DEBUG: default_NTDD: {}\n'.format(default_NTDD))

    # for start in ['', '2021-09-15', '1975-01-24']:
    #     new_NTDD = get_time_str_n_weeks_away(10, start_date_str=start)
    #     print('DEBUG: new_NTDD: {}\n'.format(new_NTDD))

    # sys.exit(0)

    # Graph a FootBall FreeKick: As a Quadratic Equation: 
    # y = d(-a(x + b)^2 + c)
    # where a < 1.0, b ~= 10m, c ~=3m, d ~=1/40

    # xData
    length_to_goal = 30
    x_list = list(np.arange(0, length_to_goal+1, 1))
    print(f'DEBUG: x_list: array: {x_list}')

    # yInfo
    a = 0.3
    b = -20.0
    c = 120.0
    d = 0.025
    dpi = 3
    y_list = [round((d * (-a * (x_val + b)**2 + c)), dpi) for x_val in x_list]
    print(f'DEBUG: y_list: array: {y_list}')

    # Plot: Cartesian, Line
    heading = 'Experiment: A FootBall FreeKick as a MATHS Equation: y = d(-a(x+b)^2+c)'
    x_desc = 'Length on FootBallPitch, metres'
    y_desc = 'Height off Ground, metres'
    graph_fpath = './data/football_freekick.png'
    fwidth = 10
    fheight = 4
    plot_2d_cartesian(
        x_list, y_list, title=heading, xlabel=x_desc, ylabel=y_desc,
        figwidth=fwidth, figheight=fheight, out_path=graph_fpath
    )

    sys.exit(0)

    # reading from a config, ini file
    conf_ini_file = './configs/sample_config.ini'
    print_file_contents(conf_ini_file)
    read_ini_config_file(conf_ini_file)

    epoch_time = 1554723620
    timestr = convert_epoch_to_datetime(epoch_time)
    print('\nDEBUG: timestr for: {}'.format(epoch_time))
    pprint(timestr)
    print('\n')

    # testing log parsing/gardening module.
    # logfile = "./logs/sample_service_log.txt"
    logfile = "./logs/geckodriver.log"

    # logchunks = []
    # limit = 3
    # while len(logchunks) < limit:
    #     chunk = log_gardening.readlog_chunks(logfile, chunksize=40)
    #     print('\nDEBUG: log chunk:')
    #     pprint([line for line in chunk])
    #     logchunks.append([line for line in chunk])
    # print('\nDEBUG: log chunk:')
    # pprint(logchunks)

    # log_gardening.printlog_lines(logfile)
    log_gardening.printlog_lines_head(logfile, 12)

    # valid_h_numbytes = [2, 20, 60, 100]
    # for vh_numbytes in valid_h_numbytes:
    #     head = log_gardening.readlog_head(logfile, numbytes=vh_numbytes)
    #     print('\n{}: HEAD: {} bytes'.format(logfile, vh_numbytes))
    #     pprint(head)

    # chunkbytes = 400
    # offstart = 50
    # chunk = log_gardening.readlog_offsetchunk(logfile, offset=offstart, numbytes=chunkbytes)
    # print('\nCHUNK {} bytes, offset from {} of {}'.format(chunkbytes, offstart, logfile))
    # pprint(chunk)

    # valid_t_numbytes = [1, 10, 30, 40]
    # for vt_numbytes in valid_t_numbytes:
    #     tail = log_gardening.readlog_tail(logfile, numbytes=vt_numbytes)
    #     print('\n{}: TAIL: {} bytes'.format(logfile, vt_numbytes))
    #     pprint(tail)

    # # invalid_numbytes = [100000000000, 0, -1, -100, 0.01]
    # # for numbytes in invalid_numbytes:
    # #     print('\nverify: input validation: numbytes: {}'.format(numbytes))
    # #     output = log_gardening.readlog_head(logfile, numbytes)
    # #     print('output: {}'.format(repr(output)))


if __name__ == '__main__':
    main()
