#!usr/bin/python

import math
import pytest
# from log_modules import log_gardening

valid_pairs = [(7, 49), (2, 4), (1, 1), (0, 0)]
@pytest.mark.parametrize("p_sqrt, num", valid_pairs)
def test_sqrt(num, p_sqrt):
   assert math.sqrt(num) == p_sqrt

@pytest.mark.parametrize("num, p_square", valid_pairs)
def test_square(num, p_square):
   print(num**2)
   err_msg = "invalid pair: ({}, {})".format(num, p_square)
   assert num**2 == p_square, err_msg

valid_eq_pairs = [(127127127127127, 127127127127127), (7, 7), (2, 2), (1, 1)]
@pytest.mark.parametrize("num1, num2", valid_eq_pairs)
def test_equality_ints(num1, num2):
   err_msg = "{} not equal to {}".format(num1, num2)
   assert num1 == num2, err_msg
