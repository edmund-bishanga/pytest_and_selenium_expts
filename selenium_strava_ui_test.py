#!/usr/bin/python

"""
Web UI Test Automation Experiments: Selenium
"""

# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

import json
from pprint import pprint

import pytest
from msedge.selenium_tools import Edge, EdgeOptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

URL = 'https://www.strava.com'
USERNAME = 'me.bishanga@gmail.com'
CRD = 'foobar1234'
STD_WAIT_SECONDS = 20
MAL_EXIT_CODE = 1
SUPPORTED_BROWSERS = ['chrome', 'firefox', 'edge']
ENV_CONFIG_FILE = './configs/env_config.json'

class UnsupportedBrowserException(Exception):
    pass

def login_as_subscriber(browser, username, pswd):
    """ Log in as specified user, in provided browser. """
    print(f'\nDEBUG: Logging in as "{username}"')
    login_button = browser.find_element(By.CLASS_NAME, 'btn-login')
    login_button.send_keys(Keys.RETURN)
    browser.implicitly_wait(STD_WAIT_SECONDS)
    email_textbox = browser.find_element(By.ID, 'email')
    email_textbox.send_keys(username + Keys.TAB)
    crd_textbox = browser.find_element(By.ID, 'password')
    crd_textbox.send_keys(pswd + Keys.RETURN)

def interact_with_cookies_banner(browser, accept=True):
    """ Accept or reject cookies: per user's choice. """
    print(f'\nDEBUG: Interacting with Cookies Banner: Accept: {accept}')
    # if accept: click on appropriate button.
    if accept:
        cookie_accept_btn = browser.find_element(By.CLASS_NAME, 'btn-accept-cookie-banner')
        cookie_accept_btn.click()

def get_user_credentials(username='default_user'):
    with open(ENV_CONFIG_FILE, 'r', encoding='UTF-8') as env_config_file:
        env_config = json.load(env_config_file)
    user_email = env_config.get(username).get('email')
    user_pswd = env_config.get(username).get('pswd')
    print(f'\nDEBUG: user_email: {user_email}, user_pswd: {user_pswd}')
    return (user_email, user_pswd)

def run_selenium_py_website_basics(browser_name):
    """ Action basic web UI user actions, using Selenium WebDriver. """
    browser = get_supported_browser(browser_name)
    browser.get(URL)
    try:
        # login_as_subscriber(browser, USERNAME, CRD)
        user_email, user_pswd = get_user_credentials()
        login_as_subscriber(browser, user_email, user_pswd)
        for val in [False, True]:
            interact_with_cookies_banner(browser, accept=val)
    except Exception as exc:  # pylint: disable=broad-except
        print('\nDEBUG: Exception observed... Details: See below...')
        pprint(exc)
    finally:
        print('\nDEBUG: Closing browser...')
        browser.close()
        print('Thank you.\n')

def get_supported_browser(name):
    """ Return browser obj or appropriate err_msg. """
    # WebDriverLocation: in PATH: C:\Drivers\webdrivers
    if name.lower() == 'chrome':
        return webdriver.Chrome()
    if name.lower() == 'firefox':
        return webdriver.Firefox()
    if name.lower() == 'edge':
        options = EdgeOptions()
        options.use_chromium = True
        return Edge(options=options)
    help_txt = f"Please try again: supported browsers: {SUPPORTED_BROWSERS}"
    print(f"Unsupported browser: {name}, {help_txt}")
    raise UnsupportedBrowserException()

@pytest.mark.parametrize('browser', SUPPORTED_BROWSERS)
def test_get_supported_browser_positive(browser):
    print(f'\nDEBUG: Browser under Test: supported: {browser.capitalize()}')
    try:
        browser_obj = get_supported_browser(browser)
    finally:
        browser_obj.close()

unsupported_browsers = ['safari', 'opera', 'ie']
@pytest.mark.parametrize('browser', unsupported_browsers)
def test_get_supported_browser_negative(browser):
    print(f'\nDEBUG: Browser under Test: unsupported: {browser.capitalize()}')
    with pytest.raises(UnsupportedBrowserException):
        get_supported_browser(browser)


def main():
    """ StartingPoint: Selenium Experiments """
    for browser in SUPPORTED_BROWSERS:
        print(f'\nDEBUG: Browser: {browser.capitalize()}')
        run_selenium_py_website_basics(browser)


if __name__ == '__main__':
    main()
