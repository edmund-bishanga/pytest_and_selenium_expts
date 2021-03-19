#!usr/bin/python

"""
Misc Experiments:
+ log file processing
+ pytest, etc
"""
# pylint: disable=missing-function-docstring

from configparser import ConfigParser
# import log_gardening
from pprint import pprint

import pytest


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

def main():
    """ Misc Experiments, testing modules """
    print('this is the main program... Ta!')

    conf_ini_file = './sample_config.ini'
    config = ConfigParser()
    config_data = config.read(conf_ini_file)
    print('DEBUG: config data'); pprint(config_data)

    print('Config: Sections: ', config.sections())
    print('Config: param: str: ', config.get('build', 'library'))
    print('Config: int: ', config.get('operation', 'timeout'))
    print('Config: bool: ', config.get('operation', 'offset'))

    # # testing log parsing/gardening module.
    # logfile = "./sample_service_log.txt"
    # # logchunks = []
    # # limit = 3
    # # while len(logchunks) < limit:
    # #     chunk = log_gardening.readlog_chunks(logfile, chunksize=40)
    # #     logchunks.append([line for line in chunk])
    # # pprint(logchunks)

    # # log_gardening.printlog_lines(logfile)

    # chunkbytes = 200
    # offstart = 50

    # head = log_gardening.readlog_head(logfile, numbytes=chunkbytes)
    # print('\nHEAD {} bytes of: {}'.format(chunkbytes, logfile))
    # pprint(head)

    # chunk = log_gardening.readlog_offsetchunk(logfile, offset=offstart, numbytes=chunkbytes)
    # print('\nCHUNK {} bytes, offset from {} of {}'.format(
    #     chunkbytes, offstart, logfile
    #     )
    # )
    # pprint(chunk)

    # tail = log_gardening.readlog_tail(logfile, numbytes=chunkbytes)
    # print('\nTAIL {} bytes of: {}'.format(chunkbytes, logfile))
    # pprint(tail)

    # print('\n')

    # invalid_numbytes = [-100, 100000000000, 0, -1, 0.01]
    # for numbytes in invalid_numbytes:
    #     print('verify: input validation: numbytes: {}'.format(numbytes))
    #     output = log_gardening.readlog_head(logfile, numbytes)
    #     print('output: {}'.format(repr(output)))

if __name__ == '__main__':
    main()
