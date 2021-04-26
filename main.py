#!usr/bin/python

"""
Misc Experiments:
+ log file processing
+ pytest, etc
"""
# pylint: disable=missing-function-docstring

# imports: Std, 3rdParty, CustomLocal
from configparser import ConfigParser
from pprint import pprint

import pytest

from modules import log_gardening


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

def read_config_file(conf_ini_file):
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


def main():
    """ Misc Experiments, testing modules """

    # # reading from a config, ini file
    # conf_ini_file = './sample_config.ini'
    # print_file_contents(conf_ini_file)
    # read_config_file(conf_ini_file)

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
