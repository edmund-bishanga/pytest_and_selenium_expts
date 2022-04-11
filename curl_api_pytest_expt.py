#!/usr/bin/python

"""
Misc QA Automation Experiments:
+ curl
+ API testing
"""
# pylint: disable=missing-function-docstring
# pylint: disable=use-list-literal
# pylint: disable=unused-import

# Imports: Recommended Order: Std, 3rdParty, CustomLocal
import json
import os
from pprint import pprint

import pytest
import yaml
from yaml.loader import SafeLoader

# 0. InputData: strings, JSON
# Config: Environment
TEST_DATA_ROOT = './data'
CLIENT_CERT_PATH = f'{TEST_DATA_ROOT}/client_public.crt'  # Get a valid one
CA_CERT_PATH = f'{TEST_DATA_ROOT}/ca-bundle.crt'
CLIENT_PRKEY_PATH = f'{TEST_DATA_ROOT}/client_private.key'
DUMMY_DATA_PATH = f'{TEST_DATA_ROOT}/sampleDummyRequestSad.xml'
SAMPLE_RESPONSE_FILE = f'{TEST_DATA_ROOT}/sample_curl_response_data.txt'
SAMPLE_RESPERR_FILE = f'{TEST_DATA_ROOT}/sample_curl_response_data_err.txt'
SERVER_ADDRESS = 'server_host_addr.co.uk'
ROOT_DEST_URL = f'https://{SERVER_ADDRESS}/api'

# Config: Settings::Defaults
DEF_IO_UTIL = 'curl'
DEF_CERTLESS_OPTIONS = ['-v', '-k']
DEF_API_OPTIONS = [
    '-vvv',
    f'--cert {CLIENT_CERT_PATH}',
    f'--key {CLIENT_PRKEY_PATH}'
]
DEF_MTLS_OPTIONS = [
    f'--cacert {CA_CERT_PATH}',
    f'--key {CLIENT_PRKEY_PATH}',
    '--key-type PEM'
]
DEF_ENCODING = 'UTF-8'
DEF_HEADER = f'Content-Type:text/xml;charset={DEF_ENCODING}'

# TestData: JSON: Extensible Test Coverage
DEF_TEST_DATA_JSON_FILE = f'{TEST_DATA_ROOT}/example_input_test_data.json'
DEF_ORG_CODE = 'ABC123'
DEF_FACTORY_CODE = 'E03'
DEF_PROD_CODE = 'EFG'
DEF_EXP_EPR_API_RESPONSE = [
    '<?xml ',
    f'encoding="{DEF_ENCODING}"',
    '<abcApi ',
    '</abcApi>'
]
DEF_TEST_DATA = {
    'serviceStatus': {
        'apiOptions': [],
        'apiPath': 'serviceStatus',
        'expSubStrings': DEF_EXP_EPR_API_RESPONSE
    },
    'sampleDummyRequest': {
        "apiOptions": [
            '-X POST', f'--header "{DEF_HEADER}"',
            f'--data-binary {TEST_DATA_ROOT}/sampleDummyRequestEFG.xml'
        ],
        'apiPath': 'sampleDummyRequest',
        'expSubStrings': DEF_EXP_EPR_API_RESPONSE
    },
    'createEFG': {
        "apiOptions": [
            '-X POST', f'--header "{DEF_HEADER}"',
            f'--data-binary {TEST_DATA_ROOT}/createEFG.xml'
        ],
        'apiPath': 'createCMA',
        'expSubStrings': DEF_EXP_EPR_API_RESPONSE
    },
    'checkJobStatus': {
        "apiOptions": [
            '-X POST', f'--header "{DEF_HEADER}"',
            f'--data-binary {TEST_DATA_ROOT}/checkJobStatus.xml'
        ],
        'apiPath': 'checkJobStatus',
        'expSubStrings': DEF_EXP_EPR_API_RESPONSE
    },
    'downloadMakersList': {
        'apiOptions': [],
        'apiPath': 'downloadManufacturersList',
        "apiParams": {
            "orgCode": DEF_ORG_CODE,
            "manufacturerCode": DEF_FACTORY_CODE,
            "productType": DEF_PROD_CODE
        },
        'expSubStrings': ['SUCCESS']
    },
}


# HelperFunctions
def set_default_api_options(cert_status, add_ca_cert):
    def_options = DEF_API_OPTIONS
    if cert_status == 'no_cert':
        def_options = DEF_CERTLESS_OPTIONS
    elif cert_status == 'insecure_cert':
        def_options = ['-k'] + DEF_API_OPTIONS
    if add_ca_cert:
        def_options += DEF_MTLS_OPTIONS
    return def_options

def get_json_test_data(json_file):
    with open(json_file, 'r', encoding=DEF_ENCODING) as inputs_file:
        t_data = json.load(inputs_file)
    print('\nDEBUG: test_data: JSONDict')
    pprint(t_data)
    return t_data

def add_api_params_to_path(api_path, api_params_dict):
    # apiPath + '?' + prm1=val1 + '&' + 'prm2=val2' + ... + '&' + 'prmN=valN'
    param_pairs = [f'{param}={val}' for param, val in api_params_dict.items()]
    api_path += '?' + '&'.join(param_pairs)
    return api_path

def form_valid_api_call_str(
        api_path_key, test_data, add_ca_cert=False, cert_status='secure_cert'
    ):
    _def_options = set_default_api_options(cert_status, add_ca_cert)
    api_options = test_data.get(api_path_key).get('apiOptions')
    _options_str = ' '.join(_def_options + api_options)
    print(f'\nDEBUG: api_options_str: {_options_str}')

    api_path_suffix = test_data.get(api_path_key).get('apiPath')
    params_dict = test_data.get(api_path_key).get('apiParams')
    if params_dict:
        api_path_suffix = add_api_params_to_path(api_path_suffix, params_dict)

    api_call = f'{DEF_IO_UTIL} {_options_str} {ROOT_DEST_URL}/{api_path_suffix}'
    print(f'\nDEBUG: {api_path_key}: API Call: \n{api_call}')
    return api_call

def get_sample_response_data(rfile_path):
    with open(rfile_path, encoding=DEF_ENCODING, mode='r') as res_file:
        response = res_file.read()
    return response

def run_api_call(api_str):
    response = os.popen(api_str).read()
    # response = get_sample_response_data(SAMPLE_RESPONSE_FILE)
    print(f'\nDEBUG: Response: \n"{response}"')
    return response

def verify_api_response(api_path, response, exp_response_substrs):
    err_msg = f'{api_path}: erroneous API response: \n{response}'
    if response == '':
        err_msg = f'{api_path}: empty API response: "{response}"'
    for must_contain_str in exp_response_substrs:
        assert must_contain_str in response, err_msg

def verify_mtls_handshake_completed(mtls_response, cert_status):
    help_txt = 'Pls Check mTLS SetUp|Config|Certs e.g. erroneous Client Cert'
    err_msg = f'mTLS HandShake Err: {help_txt}\nDetails:\n{mtls_response}'
    if cert_status in ['no_cert']:
        assert not mtls_response, err_msg
    else:
        assert mtls_response, err_msg


# Key TestCases
js_test_data = get_json_test_data(DEF_TEST_DATA_JSON_FILE)

cert_test_coverage = ['no_cert', 'insecure_cert', 'secure_cert']
@pytest.mark.parametrize('cert_status', cert_test_coverage)
def test_mutual_tls_config_no_cert_no_response(cert_status):
    api_str = form_valid_api_call_str(
        'serviceStatus', js_test_data,
        add_ca_cert=False, cert_status=cert_status
    )
    mtls_response = run_api_call(api_str)
    verify_mtls_handshake_completed(mtls_response, cert_status)

@pytest.mark.parametrize('api_path_key', js_test_data.keys())
def test_api_call_mtls_valid(api_path_key):
    api_str = form_valid_api_call_str(
        api_path_key, js_test_data, cert_status='insecure_cert'
    )
    response = run_api_call(api_str)
    exp_substrs = js_test_data.get(api_path_key).get('expSubStrings')
    verify_api_response(
        api_path_key, response, exp_response_substrs=exp_substrs
    )
