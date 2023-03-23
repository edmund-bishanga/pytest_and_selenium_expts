#!/usr/bin/python

"""
Unit Tests for methods in Class: log_gardening.LogGardening
+ run unit test on cmdline:
  python -m unittest discover -v -s <test_dir>
+ or via pytest:
  python -m pytest -v <test_dir>

+ to import custom modules seamlessly:
  * package directories should have empty __init__.py file
  * add parent/root repo dir to PYTHONPATH or Sys.PATH
    searchable by python import function
"""

import io
import os
from contextlib import redirect_stdout
from unittest import TestCase as tc

from log_modules.log_gardening import LogGardening

LOGS_DIR = os.path.join(os.curdir, '..', 'logs')
DEF_LOGFILE = os.path.join(LOGS_DIR, 'sample_service_log.txt')
GECKO_LOGFILE = os.path.join(LOGS_DIR, 'geckodriver.log')
INVALID_NUMBYTES = [
    -100,
    -100000000000,
    0,
    -1
]
INVALID_PATHS = [
    '123',
    'abc',
    '@',
    './invalid_dir/sample_service_log.txt'
]

class TestLogGardening(tc):
    """ UnitTestingClass: for methods in LogGardening Class """

    def setUp(self):
        # create relevant|necessary obj instances & pre-requisites
        self.log_handler = LogGardening(logfile_path=GECKO_LOGFILE)

    def test_printlog_lines_head_valid(self):
        # for each valid input set, validate num_lines printed
        print(f'\nDEBUG: logfile_path: {self.log_handler.logfile_path}')
        valid_num_lines  = [1, 10, 30, 90, 120]
        for num_lines in valid_num_lines:
            print(f'\nDEBUG: valid num_lines: {num_lines}')
            with io.StringIO() as buffer, redirect_stdout(buffer):
                self.log_handler.printlog_lines_head(num_lines)
                print(f'\nDEBUG: stdout buffer: {buffer.getvalue()}')
                err_headr = f'{self.log_handler.logfile_path}: expected content'
                tc.assertIn(
                    self,
                    member='geckodriver	INFO	Listening',
                    container=buffer.getvalue(),
                    msg=f'{err_headr}: missing'
                )
                tc.assertIsInstance(
                    self,
                    obj=buffer.getvalue(),
                    cls=str,
                    msg=f'{err_headr}: invalid type'
                )

    def test_readlog_head_invalid_input(self):
        for invalid_num in INVALID_NUMBYTES:
            print(f'\nTesting: invalid numbytes: {invalid_num}')
            with tc.assertRaises(
                self, expected_exception=AssertionError
            ) as context:
                self.log_handler.readlog_head(invalid_num)
            tc.assertTrue(self, 'numbytes' in str(context.exception))

    def test_readlog_tail_invalid_paths(self):
        for filepath in INVALID_PATHS:
            print(f'\nTesting: invalid_paths: {filepath}')
            self.log_handler.set_logfile_path(filepath)
            with tc.assertRaises(
                self, expected_exception=FileNotFoundError
            ) as context:
                self.log_handler.readlog_tail()
            tc.assertTrue(self, 'No such file' in str(context.exception))

    def tearDown(self):
        # clean up after unittest run
        pass
