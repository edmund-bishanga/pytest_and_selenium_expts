#!/usr/bin/python

"""
Interactive Script:
+ Tests APIs of 'YouTube Watch'

# youtube web RestAPI example
# 1. test URL params: t, hl, fmt
# Ref: https://webapps.stackexchange.com/questions/9863/are-the-parameters-for-www-youtube-com-watch-documented  # pylint: disable=line-too-long
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
# Example:
{
    "scenario_name": [{inputs_dict[equivalenceData, str_keys, obj_vals]}, {set/shared_expectations, exp_outputs_dict[str_keys, obj_vals]}, {result_dict[str_key, bool_val]}],

    "t_valid_green":      [{"t": ["0s", "10s", "1m15s", "0h10m03s", "123s"]}, {"exp_exit_code": 200, "exp_output_str": ""}, {"PASS": true}],
    "t_invalid_orange":      [{"t": ["-100s", "12h1m15s", "-10m03s", "abc", "#"]}, {"exp_exit_code": 403, "exp_output_str": "ERROR, TypoWarningCommunicated"}, {"PASS": false}],
    "t_catastrophic_red":      [{"t": ["-100000000000000000000000000", "", "######", "$(random(ridiculous_input))"]}, {"exp_exit_code": 503, "exp_output": "ERROR, DisasterGracefullyHandled"}, {"PASS": false}],
}
# 4. pytest, parametrize
# Example: See ./pytest_example.py in this dir.

# 5. parsing test data:
# + pandas: dataframes: from JSON, CSV datastores.

# 6. input validation?
# + simple, purposeful early asserts

# 7. cmd construction
# + key-value pairs

# 8. request -> response
# + requests

# 9. verify response details
# + real_sys_outputs vs expected_sys_outputs
# + result: PASS: True/False

# 10. Test Results Reporting:
# + Headlines: SummaryStats: PASS/FAIL Percentages, StdStats
# + Graphs: line, histo, pie: matplotlib
# + Tables: pprint, pandas: dataframes
"""

# pylint: disable=line-too-long
# pylint: disable=multiple-statements  # DEBUG statements
# pylint: disable=unused-import
# pylint: disable=invalid-name

import argparse
import json
import sys
import re
from pprint import pprint

import pandas as pd
import pytest
import requests

URL_ROOT = "https://www.youtube.com/watch"
R_DELIM = "?"
G_DELIM = "&"


def run_api_check_requests(relevant_inputs):
    """ constructs and verifies individual API CMDs; returns outputs dict """
    outputs = relevant_inputs
    print('DEBUG: relevant_inputs:'); pprint(relevant_inputs)
    for key in relevant_inputs:
        print(relevant_inputs[key])

        results = list()
        for val in relevant_inputs[key][0]:
            # form API cmd components
            # + root URL, params dict
            params = {key.split('_')[0]: val}
            print('\nDEBUG: params:'); pprint(params)

            # run it
            response = requests.get(URL_ROOT, params)
            print('DEBUG: URL'); print(response.url)
            print('DEBUG: response: status_code'); pprint(response.status_code)
            print('DEBUG: response: encoding'); pprint(response.encoding)
            # print('DEBUG: response: binary content'); pprint(response.content)
            # print('DEBUG: response: text'); pprint(response.text)

            # verify outcome
            outcome = 'FAIL'
            if response.status_code == 200 and 'YouTube' in response.text:
                outcome = 'PASS'
            results.append(outcome)

        print('DEBUG: results'); pprint(results)
        outputs[key].append(results)

        # err_msg = "unexpected result: {}".format(key)
        # assert outcome == relevant_inputs[key][-1], err_msg
        print('\nDEBUG: outputs'); pprint(outputs)
    return outputs

def run_api_check_requests_pandas(rel_inputs_key, rel_inputs_df):
    """ constructs and verifies individual API CMDs; returns outputs dict """
    outputs_df = rel_inputs_df
    print('DEBUG: rel_inputs_df:'); pprint(rel_inputs_df)
    for row in rel_inputs_df.index:
        row_data = rel_inputs_df.loc[row]
        print('\nDEBUG: row_data: '); pprint(row_data)

        # results = list()
        # for val in relevant_inputs[key][0]:
        #     # form API cmd components
        #     # + root URL, params dict
        #     params = {key.split('_')[0]: val}
        #     print('\nDEBUG: params:'); pprint(params)

        #     # run it
        #     response = requests.get(URL_ROOT, params)
        #     print('DEBUG: URL'); print(response.url)
        #     print('DEBUG: response: status_code'); pprint(response.status_code)
        #     print('DEBUG: response: encoding'); pprint(response.encoding)
        #     # print('DEBUG: response: binary content'); pprint(response.content)
        #     # print('DEBUG: response: text'); pprint(response.text)

        #     # verify outcome
        #     outcome = 'FAIL'
        #     if response.status_code == 200 and 'YouTube' in response.text:
        #         outcome = 'PASS'
        #     results.append(outcome)

        # print('DEBUG: results'); pprint(results)
        # outputs_df[key].append(results)

        # err_msg = "unexpected result: {}".format(key)
        # assert outcome == relevant_inputs[key][-1], err_msg
        print('\nDEBUG: outputs_df'); pprint(outputs_df)
    return outputs_df


def run_api_check(relevant_inputs):
    """ constructs and verifies individual API CMDs; returns outputs dict """
    outputs = relevant_inputs
    for key in relevant_inputs:
        print(relevant_inputs[key])

        # form API cmd
        # api_key = key.split('_')[0]
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
        err_msg = "unexpected result: {}".format(key)
        assert outcome == relevant_inputs[key][-1], err_msg
    print('\nDEBUG: outputs'); pprint(outputs)
    return outputs

@pytest.mark.skip(reason='not pytest format, a python test method')
def test_api_athlete(inputs_json_file):
    """ reads and tests each JSON key-value pair provided """
    # read json input
    with open(inputs_json_file, 'r') as inputs_file:
        inputs_data = json.load(inputs_file)
    print('\nDEBUG: inputs_data'); pprint(inputs_data)

    # get relevant test input data
    relevant_inputs = dict()
    for key in inputs_data:
        t_regex = r'^t_*.*'
        if re.search(t_regex, key):
        # if 't_' in key:
            relevant_inputs[key] = inputs_data[key]
    print('\nDEBUG: relevant_inputs'); pprint(relevant_inputs)

    # validate input data
    # validation: check that inputs list is not empty
    relevant_input_dfs = list()
    relevant_input_keys = list()
    relevant_output_dfs = list()
    for key in relevant_inputs:
        relevant_input_keys.append(key)
        inputs_df = pd.DataFrame(relevant_inputs[key])
        print('\nDEBUG: inputs_df: ', key); pprint(inputs_df, width=400)
        print('\nDEBUG: inputs_df: row labels/indices ', key); pprint(inputs_df.index, width=400)
        print('\nDEBUG: {}: row_index_name: {}'.format(key, 1)); pprint(inputs_df.loc[1])
        print('\nDEBUG: inputs_df: columns', key); pprint(inputs_df.columns, width=400)
        relevant_input_dfs.append(inputs_df)
        outputs_df = run_api_check_requests_pandas(key, inputs_df)
        relevant_output_dfs.append(outputs_df)
    print('\nDEBUG: relevant inputs: data frames: '); pprint(relevant_input_dfs, width=400)
    print('\nDEBUG: relevant inputs: df names: '); pprint(relevant_input_keys)
    print('\nDEBUG: relevant outputs: data frames: '); pprint(relevant_output_dfs, width=400)

    sys.exit(0)

    # run test: get system_response, verify response, report verdict
    # run_api_check(relevant_inputs)
    # run_api_check_requests(relevant_inputs)


def main():
    """ Interactive function: API Testing. """

    # Input validation
    args = argparse.ArgumentParser()
    args.add_argument(
        '-f', "--input-file", default='./data/test_data_youtube_web_api.json',
        help='str: path to JSON inputs file'
    )
    inputs = args.parse_args()
    print('\nInput validation:')
    pprint(inputs)

    # Test APIs
    test_api_athlete(inputs.input_file)


if __name__ == '__main__':
    main()
