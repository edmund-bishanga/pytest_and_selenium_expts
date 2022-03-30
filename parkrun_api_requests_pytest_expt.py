#!/usr/bin/python

"""
API Testing Experiment: Python
+ requests
+ pytest
+ nose
"""

# pylint: disable=missing-function-docstring
# pylint: disable=unused-import
# pylint: disable=fixme # ToDos

from pprint import pprint

import pytest
import requests
from nose.tools import assert_true


# TEST PARKRUN API:
# Sample URL: https://www.parkrun.org.uk/peel/results/weeklyresults/?
# runSeqNumber=24&utm_medium=email&utm_source=resultsemail&utm_campaign=systememail

# + api_url:
#   * root_url: https://www.parkrun.org.uk
#   * mid_url: peel, results, weeklyresults
#   * url_delimiter: '/'
ROOT_TEST_URL = 'https://www.parkrun.org.uk'
MID_TEST_URL = ['peel', 'results', 'weeklyresults']
TEST_URL_DELIMITER = '/'
API_REQ_DELIMITER = '&'
API_REQ_KVP_JOINER = '='

# + API KVPs:
#   * runSeqNumber: str_int: e.g. '24'
#   * utm_medium: str_string: e.g. 'email'
#   * utm_source: str_string: e.g. 'resultsemail'
#   * utm_campaign: str_string: e.g. 'systememail'
#   ToDo: convert to JSON: readable, scalable
DEF_INPUT_TEST_DATA = {
    'green_scenario1': {
        'runSeqNumber': '24',
        'utm_medium': 'email',
        'utm_source': 'resultsemail',
        'utm_campaign': 'systememail',
        'exp_status_code': 200,
        'exp_content_str': 'OK',
        'exp_response_timeout_ms': 5000
    },
    'green_scenario2': {
        'runSeqNumber': '100',
        'utm_medium': 'email',
        'utm_source': 'resultsemail',
        'utm_campaign': 'systememail',
        'exp_status_code': 200,
        'exp_content_str': 'OK',
        'exp_response_timeout_ms': 5000
    },
    'red_scenario1': {
        'runSeqNumber': '-1',
        'utm_medium': '',
        'utm_source': '',
        'utm_campaign': '',
        'exp_status_code': 501,
        'exp_content_str': '',
        'exp_response_timeout_ms': 3000
    },
    'red_scenario2': {
        'runSeqNumber': 'Aa;islkfnafagjia;saf;lj',
        'utm_medium': '',
        'utm_source': '',
        'utm_campaign': '',
        'exp_status_code': 501,
        'exp_content_str': '',
        'exp_response_timeout_ms': 3000
    },
    'amber_scenario1': {
        'runSeqNumber': '0',
        'utm_medium': 'inv_email',
        'utm_source': 'inv_resultsemail',
        'utm_campaign': 'inv_systememail',
        'exp_status_code': 501,
        'exp_content_str': '',
        'exp_response_timeout_ms': 3000
    },
    'amber_scenario2': {
        'runSeqNumber': 'ABC',
        'utm_medium': 'inv_email',
        'utm_source': 'inv_resultsemail',
        'utm_campaign': 'inv_systememail',
        'exp_status_code': 501,
        'exp_content_str': '',
        'exp_response_timeout_ms': 3000
    },
}

# + EquivalencePartitionsData, Priority|CriticalScenarios:
#   * Green: should work OK
#   * Red: should fail sooner, cleaner, securely, with clear WHY.
#   * Amber: should fail gracefully, with clear WHY & what to do next|helpText.
#   ToDo: Do the TestCoverage Analysis: Early...
# EQUIPART_SCALABLE_INPUT_TEST_DATA = {
#     'runSeqNumber': ['24', '1', '1000', '0', '-1'],
#     'utm_medium': ['email', 'sms', 'whatsapp'],
#     'utm_source': ['resultsemail', 'resultssms', 'resultswhatsapp'],
#     'utm_campaign': ['systememail', 'systemsms', 'systemwhatsapp']
# }


# + TestLogic
# * run API I/O: requests, JSON
# * verify API response
#   > response: functional: status_code vs expected
#   > response: functional: content vs expected
#   > response: non-functional: performance: time|duration vs expected
input_req_data = DEF_INPUT_TEST_DATA
@pytest.mark.parametrize('scenario', input_req_data.keys())
def test_parkrun_api(scenario):
    scenario_data = DEF_INPUT_TEST_DATA.get(scenario)
    api_url = ROOT_TEST_URL + '/' + '/'.join(MID_TEST_URL)
    scenario_json_kvps = dict()
    for key in scenario_data:
        if 'exp_' not in key:
            scenario_json_kvps[key] = scenario_data.get(key)
    api_response = requests.get(url=api_url, json=scenario_json_kvps)
    assert api_response.status_code == scenario_data.get('exp_status_code')
    assert scenario_data.get('exp_content_str') in api_response.text
    exp_timeout_seconds = scenario_data.get('exp_response_timeout_ms') / 1000
    assert api_response.elapsed.total_seconds() < exp_timeout_seconds
