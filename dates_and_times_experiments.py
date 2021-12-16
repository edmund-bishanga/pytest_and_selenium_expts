#!/usr/bin/python

"""
Misc Experiments:
+ Dates, Time
+ pytest
"""

# pylint: disable=missing-function-docstring
# pylint: disable=use-list-literal

# imports: Std, 3rdParty, CustomLocal
import sys
import time
from datetime import date, timedelta
from pprint import pprint

import pytest

DEF_ENCODING = 'utf-8'


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

def main():
    """ Experiment with Dates, Time. """

    default_due_date = get_time_str_n_weeks_away(10)
    print('DEBUG: default_due_date: {}\n'.format(default_due_date))

    for start in ['', '2021-09-15', '1975-01-24']:
        new_NTDD = get_time_str_n_weeks_away(10, start_date_str=start)
        print('DEBUG: new_NTDD: {}\n'.format(new_NTDD))


if __name__ == '__main__':
    main()
