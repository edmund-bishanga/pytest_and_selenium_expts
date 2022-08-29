#!/usr/bin/python

"""
Misc Experiments:
+ Dates, Time
+ pytest
"""

# pylint: disable=missing-function-docstring

# imports: Std, 3rdParty, CustomLocal
import time
from datetime import date, timedelta
from pprint import pprint

import pytest

DEF_ENCODING = 'utf-8'
DEF_NUMWEEKS = 10
SAMPLE_DATES = ['', '2021-09-15', '1975-01-24']
SAMPLE_JSON_DICT = {
        'a': {'tc_id': 'a', 'key1': 'aa', 'key2': 'bba3', 'key3': 'cc'},
        'b': {'tc_id': 'b', 'key1': 'aab', 'key2': 'bb4', 'key3': 'ccb'},
        'c': {'tc_id': 'c', 'key1': 'aac', 'key2': 'bb1', 'key3': 'ccc'}
    }

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
    start_date = date.today()
    if start_date_str:
        start_date = date.fromisoformat(start_date_str)
    print('DEBUG: start_date: ', start_date)
    # calculate date n weeks forward
    print('DEBUG: n_weeks: ', n_weeks)
    n_wks_date = start_date + timedelta(weeks=n_weeks)
    return n_wks_date

def order_dlist_by_shared_kvalue(dlist, order_by=None, direction=None):
    # order dlist, by key value
    ordered_dlist = dlist
    ordered_dlist.sort(key=lambda item: item.get(order_by))
    return ordered_dlist

def transform_json_dict_to_dlist(json_dict, hlabel='name'):
    for key in json_dict:
        json_dict.get(key).update({hlabel: key})
    dlist = [json_dict.get(key) for key in json_dict]
    return dlist

def dbg_print(obj, text):
    print(f'\nDEBUG: {text}:')
    pprint(obj)

def main():
    """ Experiment with Dates, Time. """

    # Evaluate dates and weeks diffs
    default_due_date = get_time_str_n_weeks_away(DEF_NUMWEEKS)
    dbg_print(default_due_date, 'default_due_date')
    for start in SAMPLE_DATES:
        new_ntdd = get_time_str_n_weeks_away(DEF_NUMWEEKS, start_date_str=start)
        dbg_print(new_ntdd, 'new_NTDD')

    # Transform a json_dict into a dlist
    dlist = transform_json_dict_to_dlist(SAMPLE_JSON_DICT, hlabel='tc_id')
    # dlist: sort by values of a specific key
    for key in ['tc_id', 'key2', 'key1']:
        ordered_dlist = order_dlist_by_shared_kvalue(dlist, order_by=key)
        dbg_print(ordered_dlist, f'ordered_list: by values of {key}')


if __name__ == '__main__':
    main()
