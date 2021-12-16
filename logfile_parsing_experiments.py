#!/usr/bin/python

"""
Misc Experiments:
+ log file processing
+ pytest, etc
"""

# pylint: disable=missing-function-docstring
# pylint: disable=use-list-literal


# imports: Std, 3rdParty, CustomLocal
import sys
import time
from datetime import date, timedelta
from pprint import pprint

import pytest

from log_modules.log_gardening import LogGardening

DEF_ENCODING = 'utf-8'

def print_file_contents(filepath):
    with open(filepath, 'r', encoding=DEF_ENCODING) as file:
        content = file.read()
    delim = '++++++++++++++++++++'
    print(delim)
    print(content)
    print(delim)

def main():
    """ Log Parsing Experiments. """

    # TESTING LOG PARSING/GARDENING MODULE
    # logfile = "./logs/sample_service_log.txt"
    logfile = "./logs/geckodriver.log"
    log_file_analyser = LogGardening(logfile_path=logfile)

    logchunks = []
    limit = 1
    while len(logchunks) < limit:
        chunk = log_file_analyser.readlog_chunks(chunksize=20)
        print('\nDEBUG: log chunk:')
        pprint([line for line in chunk])
        logchunks.append([line for line in chunk])
    print('\nDEBUG: log chunk:')
    pprint(logchunks)

    log_file_analyser.printlog_lines_head(num_lines=12)

    valid_h_numbytes = [2, 20, 60, 100]
    for vh_numbytes in valid_h_numbytes:
        head = log_file_analyser.readlog_head(numbytes=vh_numbytes)
        print(f'\n{logfile}: HEAD: {vh_numbytes} bytes')
        pprint(head)

    chunkbytes = 40
    offstart = 5
    chunk = log_file_analyser.readlog_offsetchunk(offset=offstart, numbytes=chunkbytes)
    print(f'\nCHUNK {chunkbytes} bytes, offset from {offstart} of {logfile}')
    pprint(chunk)

    valid_t_numbytes = [1, 10, 30, 40]
    for vt_numbytes in valid_t_numbytes:
        tail = log_file_analyser.readlog_tail(numbytes=vt_numbytes)
        print(f'\n{logfile}: TAIL: {vt_numbytes} bytes')
        pprint(tail)

    invalid_numbytes = [100000000000, 0, -1, -100, 0.01]
    for numbytes in invalid_numbytes:
        print(f'\nverify: input validation: numbytes: {numbytes}')
        try:
            output = log_file_analyser.readlog_head(numbytes)
            print(f'output: {repr(output)}')
        except AssertionError as AsstErr:
            pprint(AsstErr)


if __name__ == '__main__':
    main()
