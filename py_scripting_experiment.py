#!/usr/bin/python
""" Misc Python Test Experiments """

# pylint: disable=missing-function-docstring

# imports
from __future__ import print_function

import sys

# TEST EXPERIMENT
# Return expected key presses for a multi-press keypad
# https://en.wikipedia.org/wiki/Telephone_keypad#/media/File:Telephone-keypad2.svg
#
#   -------------------------
#   |       |  ABC  |  DEF  |
#   |   1   |   2   |   3   |
#   -------------------------
#   |  GHI  |  JKL  |  MNO  |
#   |   4   |   5   |   6   |
#   -------------------------
#   | PQRS  |  TUV  | WXYZ  |
#   |   7   |   8   |   9   |
#   -------------------------
#   |       |       |       |
#   |   *   |   0   |   #   |
#   -------------------------
#
# Given a word, output the string of keypresses required.  Press a key multiple
# times to access the desired character e.g. to insert a B press 22.
#
# In order to insert two characters in sequence from the same key, the user must
# pause before pressing the key a second time. The space character ' ' should be
# printed to indicate a pause. For example, `2 2` indicates AA whereas `22`
# indicates B.
#
# Examples:
#
#   go -> 4666
#   go go -> 466604666
#   no -> 66 666
#
# Test cases are included.  Run all test cases as:
#
#   python keys.py
#
# or particular example as:
#
#   python keys.py <word>

digit_keys = {
    2: "abc",
    3: "def",
    4: "ghi",
    5: "jkl",
    6: "mno",
    7: "pqrs",
    8: "tuv",
    9: "wxyz",
    0: " ",
}

def decode_to_num_str(char):
    num_str = 'Err'
    for num_key, letters in digit_keys.items():
        if char in letters:
            num_str = str(num_key) * (letters.index(char)+1)
    return num_str

def keys_to_press(text):
    output_num_str = []
    previous = ''
    for i, char in enumerate(text):
        num_str = decode_to_num_str(char)
        if i > 0 and previous in num_str:
            output_num_str.append(' ')
        output_num_str.append(num_str)
        previous = num_str
    if 'Err' in output_num_str:
        output_num_str = 'invalid'
    return ''.join(output_num_str)

TESTS = {
    "hi": "44 444",
    "hello world": "4433555 555666096667775553",
    "youview": "99966688 888444339",
    "go": "4666",
    "go go": "466604666",
    "no": "66 666",
    "yes": "999337777",
    " ": "0",
    "  ": "0 0",
    "   ": "0 0 0",
     "a a a ": "202020",
    " a a a": "020202",
    "a  a  a": "20 020 02",
    "a  bb  ccc": "20 022 220 0222 222 222",
    ";x/k": "invalid"
}

def validate_input_text(input_text):
    input_ok = True
    invalid_chars = [';', ':', ',']
    for in_char in invalid_chars:
        err_msg = f'InputError: "{input_text}" contains "{in_char}"\n'
        if in_char in input_text:
            input_ok = False
        # assert in_char not in input_text, err_msg
    print('Input: OK' if input_ok else err_msg)

def run_test(input_text):
    """Test harness for `keys_to_press`.

    :param input_text str: Input to function
    :return test result: bool: Passed/Failed
    """
    expected_output = TESTS.get(input_text)
    print(f'Input :          "{input_text}"')
    validate_input_text(input_text)
    print(f'Expected Output: "{expected_output}"')

    output = keys_to_press(input_text)
    print(f'Output:          "{output}"')

    passed = output == expected_output
    print('PASS' if passed else '!!! ERROR')
    return passed


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_test(sys.argv[1])
    else:
        PASSED_COUNT = 0
        for input_text_key in TESTS:
            print('\n' + '+-' * 18)
            if run_test(input_text_key):
                PASSED_COUNT += 1
        print(f"\n{PASSED_COUNT} of {len(TESTS)} tests passed")
