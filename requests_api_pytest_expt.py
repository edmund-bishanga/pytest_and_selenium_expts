#!/usr/bin/python

"""
API Testing Experiment: Python
+ requests
+ pytest
+ nose
"""

# pylint: disable=missing-function-docstring

from pprint import pprint

import pytest
import requests
from nose.tools import assert_true


ROOT_TEST_URL = 'http://jsonplaceholder.typicode.com'
ROUTES = {
    'users': [
        'address', 'company', 'email', 'id', 'name',
        'username', 'website'
    ],
    'todos': ['userId', 'id', 'title', 'completed']
}


# run cmd: nosetests -v -s <filename>.py
def test_api_get_nose(routes=ROUTES.keys()):
    for route in routes:
        # Send a request to the real API server and store the response.
        api_url = ROOT_TEST_URL + f'/{route}'
        response = requests.get(api_url, params=None)

        # verify response: status_code
        assert_true(response.ok)

        # verify response: detail vs expected
        for entry in response.json():
            for expected_key in ROUTES.get(route):
                err_msg = f'Error: {entry.keys()} missing key: "{expected_key}"'
                assert expected_key in entry.keys(), err_msg

# run_cmd: pytest -v --capture=tee-sys <filename>.py
@pytest.mark.parametrize('route', ROUTES.keys())
def test_api_get_pytest(route):
    # Send a request to the real API server and store the response.
    api_url = ROOT_TEST_URL + f'/{route}'
    response = requests.get(api_url, params=None)

    # verify response: status_code
    assert response.status_code == 200

    # verify response: detail vs expected
    for entry in response.json():
        for expected_key in ROUTES.get(route):
            err_msg = f'Error: {entry.keys()} missing key: "{expected_key}"'
            assert expected_key in entry.keys(), err_msg

post_data = {
    'jane': {'name': 'Jane TAYLOR', 'email': 'jane.taylor@abc.co.uk'},
    'james': {'name': 'James BISHANGA', 'email': 'james.bishanga@abc.co.uk'}
}
@pytest.mark.parametrize('name', post_data.keys())
def test_api_post_pytest(name, route = 'users'):
    # form and send request, get response
    api_url = ROOT_TEST_URL + f'/{route}'
    response = requests.post(url=api_url, json=post_data.get(name))
    print('\nDEBUG: response: POST')
    pprint(response.json())
    # verify response: status_code
    assert response.status_code == 201

    # verify response: content detail
    assert isinstance(response.json(), dict)
    for expected_key in post_data.get(name).keys():
        assert expected_key in response.json().keys()

put_data = {
    'jane': {'email': 'updated-jane.taylor@abc.co.uk', 'id': 1},
    'james': {'email': 'changed.james.bishanga@abc.co.uk', 'id': 3}
}
@pytest.mark.parametrize('name', put_data.keys())
def test_api_put_pytest(name, route = 'users'):
    # form and send request, get response
    api_url = ROOT_TEST_URL + f'/{route}/{str(put_data.get(name).get("id"))}'
    put_data_json = {'email': put_data.get(name).get('email')}
    response = requests.put(url=api_url, json=put_data_json)

    # verify response: status_code
    assert response.status_code == 200

    # verify response: content detail
    assert isinstance(response.json(), dict)
    assert put_data.get(name).get('email') == response.json().get('email')

@pytest.mark.parametrize('name', put_data.keys())
def test_api_delete_pytest(name, route = 'users'):
    # form and send request, get response
    api_url = ROOT_TEST_URL + f'/{route}/{str(put_data.get(name).get("id"))}'
    response = requests.delete(url=api_url)
    print('\nDEBUG: response: DELETE')
    pprint(response.json())

    # verify response: status_code
    assert response.status_code == 200

    # verify response: content detail
    assert isinstance(response.json(), dict)
    assert not response.json()
