#!usr/bin/python

import math
import pytest
# import log_gardening

def test_sqrt():
   num = 25
   assert math.sqrt(num) == 5

def test_square():
   num = 7
   print(num**2)
   assert num**2 == 49, "means ABC"

@pytest.mark.parametrize("tuple", [(10, 10), (11, 11), (9, 9)])
def test_equality(tuple):
    print('Testing: {}'.format(tuple))
    assert tuple[0] == tuple[1]

# invalid_options = ['123', 'abc', '~', './sample_service_log.txt']
# @pytest.mark.parametrize("logfile_path", invalid_options)
# def test_readlog_tail_invalid_path(logfile_path='1234'):
#     print('Testing: {}'.format(logfile_path))
#     with pytest.raises(FileNotFoundError):
#         log_gardening.readlog_tail(logfile_path)

# test_readlog_tail_invalid_path()
# test_sqrt()
# test_square()
# test_equality()
