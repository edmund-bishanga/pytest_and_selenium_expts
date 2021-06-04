#!/usr/bin/python
"""
Interactive Script:
+ Tests APIs of 'YouTube Watch'

# youtube web RestAPI example
# 1. test URL params: t, hl, fmt
# Ref: https://webapps.stackexchange.com/questions/9863/are-the-parameters-for-www-youtube-com-watch-documented 
# Example: https://www.youtube.com/watch?v=6FzAexTVNt0&t=124s 

# 2. equivalence partition technique
# t: 
#   valid: int:     0s, 10s, 1m15s, 0h10m03s, 123s
#   invalid: var:   -100s, -3m10s, abc, #
# fmt: 
#   valid: int:     5, 34, 35, 18, 22, 37, 38, 43, 45, 17
#   invalid: var:   0, -1, i, #
# hl: 
#   valid: str:     en-GB, en-US, zh-TW, fr-FR, nl-NL
#   invalid: var:   abc, en-12, *h-TW, 123

# 3. json data-driven format
# 4. pytest, parametrize
# 5. input validation?
# 6. cmd construction
# 7. request -> response
# 8. verify response details
"""

# pylint: disable=line-too-long
# pylint: disable=multiple-statements  # DEBUG statements
# pylint: disable=unused-import
# pylint: disable=invalid-name

import argparse
import json
import sys
from pprint import pprint

import requests

URL_ROOT = "https://www.youtube.com/watch"
R_DELIM = "?"
G_DELIM = "&"


def run_api_check(relevant_inputs):
    outputs = relevant_inputs
    for key in relevant_inputs:
        print(relevant_inputs[key])
        # form API cmd
        api_key = key.split('_')[0]
        api_cmd = URL_ROOT + R_DELIM
        api_cmd_suffix = relevant_inputs[key][1]
        api_cmd = api_cmd + " ".join(api_cmd_suffix)
        print('API_cmd: "{}"'.format(api_cmd))

        # validate API format

        # run it
        # response = requests.get(api_cmd)
        response = {'status_code': 200, 'text': 'OK'}

        # verify outcome
        outcome = 'FAIL'
        if response["status_code"] == 200:
            outcome = 'PASS'
        outputs[key].append(outcome)
        assert outcome == relevant_inputs[key][-1], "unexpected result: {}".format(key)
    print('\nDEBUG: outputs'); pprint(outputs)
    return outputs


def test_api_athlete(inputs_json_file):
    """ API: -a, --athlete: test various inputs """
    # read json input
    with open(inputs_json_file, 'r') as inputs_file:
        inputs_data = json.load(inputs_file)
    print('\nDEBUG: inputs_data'); pprint(inputs_data)

    # get relevant test input data
    relevant_inputs = dict()
    for key in inputs_data:
        if 't_' in inputs_data[key]:
            relevant_inputs[key] = inputs_data[key]
    print('\nDEBUG: relevant_inputs'); pprint(relevant_inputs)

    # validate input data

    # run test: get system_response, verify response, report verdict
    run_api_check(relevant_inputs)


def main():
    """ Interactive function: API Testing. """
    # Input validation
    args = argparse.ArgumentParser()
    args.add_argument(
        '-f', "--input-file", default='./data/test_data_youtube_web_api.json', help='str: path to JSON inputs file'
    )
    inputs = args.parse_args()
    print('\nInput validation:')
    pprint(inputs)

    # Test APIs
    test_api_athlete(inputs.input_file)


if __name__ == '__main__':
    main()
