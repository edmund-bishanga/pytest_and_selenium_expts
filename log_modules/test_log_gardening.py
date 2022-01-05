#!/usr/bin/python

"""
Unit Tests for methods in Class: log_gardening.LogGardening
+ run unit test on cmdline:
  python -m unittest discover -v -s <test_dir>
+ or via pytest:
  python -m pytest -v <test_dir>
"""

from unittest import TestCase

import pytest

from log_gardening import DEF_LOGFILE, LogGardening


class TestLogGardening(TestCase):

    def setUp(self):
        # create relevant|necessary obj instances & pre-requisites
        self.log_handler = LogGardening()

    def test_readlog_head_invalid_input(self):
        invalid_numbytes = [-100, -100000000000, 0, -1]
        for invalid_num in invalid_numbytes:
            print(f'\nTesting: invalid numbytes: {invalid_num}')
            self.log_handler.set_logfile_path(DEF_LOGFILE)
            with TestCase.assertRaises(self, expected_exception=AssertionError) as context:
                self.log_handler.readlog_head(invalid_num)
            TestCase.assertTrue(self, 'numbytes' in str(context.exception))

    def test_readlog_tail_invalid_paths(self):
        equiv_partitions = ['123', 'abc', '@', './sample_service_log.txt']
        for filepath in equiv_partitions:
            print(f'\nTesting: {filepath}')
            self.log_handler.set_logfile_path(filepath)
            with TestCase.assertRaises(self, expected_exception=FileNotFoundError) as context:
                self.log_handler.readlog_tail()
            TestCase.assertTrue(self, 'No such file' in str(context.exception))

    def tearDown(self):
        # clean up after unittest run
        pass
