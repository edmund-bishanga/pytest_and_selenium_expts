#!usr/bin/python

import math
import pytest
from pprint import pprint

valid_pairs = [(7, 49), (2, 4), (1, 1), (0, 0)]
@pytest.mark.parametrize("p_sqrt, num", valid_pairs)
def test_sqrt(num, p_sqrt):
   """ scenario: green: DEBUG printing, during dev """
   new_obj = dict()
   new_obj.update({'abc': 123})
   print('DEBUG: new_obj')
   pprint(new_obj, width=120)
   assert math.sqrt(num) == p_sqrt

@pytest.mark.parametrize("num, p_square", valid_pairs)
def test_square(num, p_square):
   """ scenario: green: positive assertion, input data re-use """
   print(num**2)
   err_msg = f'Error: invalid pair: ({num}, {p_square})'
   assert num**2 == p_square, err_msg

valid_eq_pairs = [(127127127127127, 127127127127127), (7, 7), (2, 2), (1, 1)]
@pytest.mark.parametrize("num1, num2", valid_eq_pairs)
def test_equality_ints(num1, num2):
   err_msg = f'{num1} not equal to {num2}'
   assert num1 == num2, err_msg

valid_pallendrums = ['retter', 'abccba', 'radar', 'padap']
@pytest.mark.parametrize('input_word', valid_pallendrums)
def test_pallendrum_valid(input_word):
   """ scenario: green: test positive user input coverage """
   err_msg = f'Error: {input_word}: not a pallendrum'
   assert input_word == input_word[::-1], err_msg

invalid_pallendrums = ['aretter', 'aabccba', 'aradar', 'invalid']
@pytest.mark.parametrize('input_word', invalid_pallendrums)
def test_pallendrum_invalid(input_word):
   """ scenario: orange: tests mild erroneous user input """
   err_msg = f'Error: {input_word}: is a pallendrum'
   assert input_word != input_word[::-1], err_msg

invalid_inputs = [1, 2, 3, 4]
@pytest.mark.parametrize('input_int', invalid_inputs)
def test_expecting_exception(input_int):
   """ scenario: red: tests errorHandling: provide specificException name """
   with pytest.raises(Exception):
      input_int / 0

# Add DDT: DataDrivenTesting module experiment
import ddt
