#!/usr/bin/python
"""
Custom API Test Coverage.

Using the following:
+ pytest: as the test engine: format, runtime, reporting.
+ requests: as the key request <--> response module.
"""

# pylint: disable=missing-function-docstring  # descriptive function names OK

import logging
import os
import re

import pytest
import requests

import utils


SERVER_PORT = 5001
ROOT_DSRSP_URL = f"https://localhost:{SERVER_PORT}"
CONSUMER_URL = f"{ROOT_DSRSP_URL}/consumer"
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
SVR_CERT = os.path.join(DATA_DIR, "localhost.pem")

DEF_TIMEOUT = 120
EXP_CONSUMER_KEYS = ["address", "email", "name", "tariffID", "uniqueID"]
CLIENT_HTTP_ERR_CODES = [400, 401, 403, 404, 405]
EXP_HREADABLE_4XX_ERR_MSGS = [
    "bad request",
    "unauthorized",
    "forbidden",
    "not found",
    "method not allowed",
    "unprocessable entity",
    "validation error",
    "missing request data"
]


# Config: Logging
LOGFILE = os.path.join(RESULTS_DIR, "test_custom_api.log")
log_fmt = "%(asctime)s: %(levelname)s: %(message)s"
date_fmt = "%a/%d.%b.%Y %H:%M:%S"
logging.basicConfig(format=log_fmt, datefmt=date_fmt, level=logging.DEBUG)
log = logging.getLogger("test_custom_api")

log_file_h = logging.FileHandler(LOGFILE, encoding="utf-8", mode="w")
log_file_h.setLevel(logging.DEBUG)
log_file_h.setFormatter(logging.Formatter(fmt=log_fmt, datefmt=date_fmt))
log.addHandler(log_file_h)
log.propagate = True


def delete_consumer(consumer_id):
    api_url = CONSUMER_URL + f"/{consumer_id}"
    requests.delete(api_url, timeout=DEF_TIMEOUT, verify=SVR_CERT)

def validate_consumer_id(cid, min_len=4, max_len=32):
    exp_id_regex = r"(\w+)"
    assert re.match(exp_id_regex, cid)
    assert min_len <= len(cid) <= max_len

@pytest.mark.tidyup
def test_tidy_up():
    """
    Clear database entries created by automated tests.

    One can also simply 'truncate' the Database Tables: server-side
    Using pgadmin tool.
    """
    cids_all = [
        "a4apraygjxzyaft6q0ra7mdk",
        "ceck0okvjyj8jq8x1nkk6diu",
        "drn2f0bz8xjiyyvs02em9svb",
        "fn29bu2swjfru9f9nd2g1wjm",
        "g3zca6dvgixgb1nmjidqlezs",
        "hdzbh0jj4qj7o61hwj491qdn",
        "i8aj2b33g2z7hjgwe1fdip7f",
        "jun12xvx40up4rvtyqvvp1lu",
        "q47rse7f4rumx57iqeh4cx83",
        "skx9cka8hpkuy01voudsruwf",
        "ufhrlv7wzcpnrwmin5nqfcqt",
        "v9ulf56qpci2wr1h1druyxih",
        "vgmdzhzhle49eiudz370o2jg",
        "x14n883w2km7m2en5bqblmwn",
        "y13qgbfmopyjt5sn2z6k8fic",
        "yfpzkhsu4o3ymbi97hn3o1r5"
    ]
    cids_to_skip = [
        "g3zca6dvgixgb1nmjidqlezs",
        "vgmdzhzhle49eiudz370o2jg"
    ]
    cids_to_clean = [cid for cid in cids_all if cid not in cids_to_skip]
    log.debug("cids_to_clean: %d: \n%s", len(cids_to_clean), cids_to_clean)
    for cid in cids_to_clean:
        log.debug("cleaning: consumer_id: %s", cid)
        delete_consumer(cid)

# run_cmd: pytest -v --capture=tee-sys <filename>.py
# Test: /consumer/registration: PUT|CreateWhole
put_scenarios = utils.read_from_json_file("custom_put_scenarios.json")
valid_put_data = put_scenarios.get("valid")
@pytest.mark.parametrize("scenario", valid_put_data.keys())
@pytest.mark.acceptance
@pytest.mark.create
# @pytest.mark.skip(reason="server setup incomplete ATM")
def test_put_register_customer_valid(scenario, tidyup=False):
    log.info("TestCaseScenario: valid: %s: PUT", scenario)
    # 1: Form and send APIRequest, Retrieve APIResponse
    api_url = CONSUMER_URL + "/registration"
    log.debug("APIUrl: %s", api_url)
    put_data_json = valid_put_data.get(scenario)
    log.debug("RequestData: \n%s", put_data_json)
    response = requests.put(
        url=api_url,
        json=put_data_json,
        timeout=DEF_TIMEOUT,
        verify=SVR_CERT
    )
    log.debug("ResponseData: \n%s", response)
    if response.text:
        log.debug("ResponseData: JSON: \n%s", response.json())

    # 2: Verify APIResponse: status_code, payload_detail
    assert response.status_code == 200
    if response.text:
        consumer_id = response.json().get("uniqueId")
        validate_consumer_id(consumer_id)
        if tidyup:
            delete_consumer(consumer_id)
    log.info("Result: PUT: %s: Passed", scenario)

inv_put_data = utils.expand_klisted_dicts(put_scenarios.get("invalid"))
@pytest.mark.parametrize("scenario", inv_put_data.keys())
@pytest.mark.create
def test_put_register_customer_invalid(scenario):
    log.info("TestCaseScenario: invalid: %s: PUT", scenario)
    excl_scenarios = ["email_type", "tariffid", "uniqueid"]
    if any(val in scenario for val in excl_scenarios):
        log.debug("Skipping scenario: %s", scenario)
        return
    # 1: Form and send APIRequest, Retrieve APIResponse
    api_url = CONSUMER_URL + "/registration"
    log.debug("APIUrl: %s", api_url)
    put_data_json = inv_put_data.get(scenario)
    log.debug("RequestData: \n%s", put_data_json)
    response = requests.put(
        url=api_url,
        json=put_data_json,
        timeout=DEF_TIMEOUT,
        verify=SVR_CERT
    )
    log.debug("ResponseData: \n%s", response)
    if response.text:
        log.debug("ResponseData: JSON: \n%s", response.json())

    # 2: Verify APIResponse: status_code, payload detail
    log.debug("Response: StatusCode: %d", response.status_code)
    log.debug("Response: ErrReason: '%s'", response.reason)
    log.debug("Response: Error: %s", response.json().get("errors"))
    log.debug("Response: Detail: %s", response.json().get("detail"))
    assert response.status_code in CLIENT_HTTP_ERR_CODES
    if response.text:
        resp_title = response.json().get("title")
        log.debug("Response: ErrMsg: '%s'", resp_title)
        assert any(err_msg in resp_title.lower()
                   for err_msg in EXP_HREADABLE_4XX_ERR_MSGS)
    log.info("Result: %s: Passed", scenario)

# Test: /consumer/{consumer-id}: GET
get_scenarios = utils.read_from_json_file("custom_get_scenarios.json")
valid_get_list = get_scenarios.get("valid")
@pytest.mark.parametrize("scenario", valid_get_list)
@pytest.mark.acceptance
@pytest.mark.retrieve
def test_get_consumer_valid(scenario, setup_consumers):
    assert setup_consumers, "pre-requisite error: missing valid consumer ids."
    for c_id in setup_consumers:
        log.info("TestCaseScenario: valid: %s: %s: GET", c_id, scenario)
        # 1: Form and send APIRequest, Retrieve APIResponse
        api_url = CONSUMER_URL + f"/{c_id}"
        log.debug("APIUrl: %s", api_url)
        response = requests.get(api_url, timeout=DEF_TIMEOUT, verify=SVR_CERT)
        log.debug("ResponseData: \n%s", response)
        if response.text:
            log.debug("ResponseData: JSON: \n%s", response.json())

        # 2: Verify APIResponse: status_code, payload detail
        assert response.status_code == 200
        if response.text:
            for exp_key in EXP_CONSUMER_KEYS:
                assert exp_key in response.json().keys()
                act_val = response.json().get(exp_key)
                log.debug("key: %s: actual_val: %s", exp_key, act_val)
                assert act_val is not None
        log.info("Result: GET: %s: %s: Passed", scenario, c_id)

inv_get_list = get_scenarios.get("invalid")
@pytest.mark.parametrize("consumer_id", inv_get_list)
@pytest.mark.retrieve
def test_get_consumer_invalid(consumer_id):
    log.info("TestCaseScenario: invalid: %s: GET", consumer_id)
    # 1: Form and send APIRequest, Retrieve APIResponse
    api_url = CONSUMER_URL + f"/{consumer_id}"
    log.debug("APIUrl: %s", api_url)
    response = requests.get(api_url, timeout=DEF_TIMEOUT, verify=SVR_CERT)
    log.debug("ResponseData: \n%s", response)
    if response.text:
        log.debug("ResponseData: JSON: \n%s", response.json())

    # 2: Verify APIResponse: status_code, payload detail
    log.debug("Response: StatusCode: %d", response.status_code)
    log.debug("Response: ErrReason: '%s'", response.reason)
    assert response.status_code == 404
    if response.text:
        resp_title = response.json().get("title")
        log.debug("Response: ErrMsg: '%s'", resp_title)
        assert "not found" in resp_title.lower()
    log.info("Result: GET: %s: Passed", consumer_id)

# Test: /consumer/{consumer-id}: PATCH|UpdatePartial
patch_scenarios = utils.read_from_json_file("custom_patch_scenarios.json")
valid_patch_data = patch_scenarios.get("valid")
@pytest.mark.parametrize("scenario", valid_patch_data.keys())
@pytest.mark.acceptance
@pytest.mark.update
def test_patch_consumer_valid(scenario, setup_consumers):
    assert setup_consumers, "pre-requisite error: missing valid consumer ids."
    for c_id in setup_consumers:
        log.info("TestCaseScenario: valid: %s: %s: PATCH", c_id, scenario)
        # 1: Form and send APIRequest, Retrieve APIResponse
        api_url = CONSUMER_URL + f"/{c_id}"
        log.debug("APIUrl: %s", api_url)
        patch_data_json = valid_patch_data.get(scenario)
        log.debug("RequestData: \n%s", patch_data_json)
        response = requests.patch(
            url=api_url,
            json=patch_data_json,
            timeout=DEF_TIMEOUT,
            verify=SVR_CERT
        )
        log.debug("ResponseData: \n%s", response)
        if response.text:
            log.debug("ResponseData: JSON: \n%s", response.json())

        # 2: Verify APIResponse: status_code, payload_detail
        assert response.status_code == 200
        if response.text:
            validate_consumer_id(response.json().get("uniqueId"))
        log.info("Result: PATCH: %s: %s: Passed", scenario, c_id)

inv_scenarios = patch_scenarios.get("invalid")
invalid_patch_data = utils.flatten_keyvals_update_inv(inv_scenarios)
@pytest.mark.parametrize("consumer_id", invalid_patch_data.keys())
@pytest.mark.update
def test_patch_consumer_invalid(consumer_id):
    log.info("TestCaseScenario: invalid: %s: PATCH", consumer_id)
    # 1: Form and send APIRequest, Retrieve APIResponse
    api_url = CONSUMER_URL + f"/consumer/{consumer_id}"
    log.debug("APIUrl: %s", api_url)
    patch_data_json = invalid_patch_data.get(consumer_id)
    log.debug("RequestData: \n%s", patch_data_json)
    response = requests.patch(
        url=api_url,
        json=patch_data_json,
        timeout=DEF_TIMEOUT,
        verify=SVR_CERT
    )
    log.debug("ResponseData: \n%s", response)
    if response.text:
        log.debug("ResponseData: JSON: \n%s", response.json())

    # 2: Verify APIResponse: status_code, payload detail
    log.debug("Response: StatusCode: %d", response.status_code)
    log.debug("Response: ErrReason: '%s'", response.reason)
    assert response.status_code in CLIENT_HTTP_ERR_CODES
    if response.text:
        resp_title = response.json().get("title")
        log.debug("Response: ErrMsg: '%s'", resp_title)
        assert any(err_msg in resp_title.lower()
                   for err_msg in EXP_HREADABLE_4XX_ERR_MSGS)
    log.info("Result: %s: Passed", consumer_id)

# Test: /consumer/{consumer-id}: DELETE|Remove
del_scenarios = utils.read_from_json_file("custom_del_scenarios.json")
valid_del_list = del_scenarios.get("valid")
@pytest.mark.parametrize("scenario", del_scenarios.get("valid"))
@pytest.mark.acceptance
@pytest.mark.delete
def test_delete_consumer_valid(scenario, setup_consumers):
    assert setup_consumers, "pre-requisite error: missing valid consumer ids."
    for c_id in setup_consumers:
        log.info("TestCaseScenario: valid: %s: %s: DELETE", scenario, c_id)
        # 1: Form and send APIRequest, Retrieve APIResponse
        api_url = CONSUMER_URL + f"/{c_id}"
        log.debug("APIUrl: %s", api_url)
        response = requests.delete(
            api_url,
            timeout=DEF_TIMEOUT,
            verify=SVR_CERT
        )
        log.debug("ResponseData: \n%s", response)

        # 2: Verify APIResponse: status_code
        assert response.status_code == 200
        log.info("Result: DELETE: %s: %s: Passed", scenario, c_id)

inv_del_list = del_scenarios.get("invalid")
@pytest.mark.parametrize("consumer_id", inv_del_list)
@pytest.mark.delete
@pytest.mark.dev
def test_delete_consumer_invalid(consumer_id):
    log.info("TestCaseScenario: invalid: %s: DELETE", consumer_id)
    # 1: Form and send APIRequest, Retrieve APIResponse
    api_url = CONSUMER_URL + f"/{consumer_id}"
    log.debug("APIUrl: %s", api_url)
    response = requests.delete(
        api_url,
        params=None,
        timeout=DEF_TIMEOUT,
        verify=SVR_CERT
    )
    log.debug("ResponseData: \n%s", response)
    if response.text:
        log.debug("ResponseData: JSON: \n%s", response.json())

    # 2: Verify APIResponse: status_code
    log.debug("Response: StatusCode: %d", response.status_code)
    log.debug("Response: ErrReason: '%s'", response.reason)
    assert response.status_code == 404
    if response.text:
        resp_title = response.json().get("title")
        log.debug("Response: ErrMsg: '%s'", resp_title)
        assert "not found" in resp_title.lower()
    log.info("Result: %s: Passed", consumer_id)
