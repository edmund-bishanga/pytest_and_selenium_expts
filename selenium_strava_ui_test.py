#!/usr/bin/python

"""
Web UI Test Automation Experiments: Selenium
+ multiple browser support
"""

# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long

import json
from pprint import pprint

import pytest
from msedge.selenium_tools import Edge, EdgeOptions
from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException, InvalidSessionIdException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

URL = 'https://www.strava.com'
SUPPORTED_BROWSERS = ['chrome', 'firefox', 'edge']
ENV_CONFIG_FILE = './env/env_config.json'
STD_WAIT_SECONDS = 20
SESSION_EXCEPTIONS = (
    SessionNotCreatedException, InvalidSessionIdException,NoSuchElementException
)


class UnsupportedBrowserException(Exception):
    pass


def verify_invalid_login(browser):
    err_txt = 'username or password did not match'
    print(f'\nDEBUG: verifying text: "{err_txt}"')
    err_msg_banner = browser.find_element(By.CLASS_NAME, 'alert-message')
    assert err_txt in err_msg_banner.text

def verify_valid_login(browser):
    # + via a specific element: xpath
    print('\nDEBUG: verification by DOM element: ul -> li -> a')
    dash_a_xpath = '/html/body/header/nav/div[2]/ul[1]/li[1]/a'
    dash_link = browser.find_element_by_xpath(dash_a_xpath)
    print(dash_link.get_attribute('href'))
    assert 'dashboard' in dash_link.get_attribute('href')
    # + via a specific element: ccs selector: more readable
    dash_a_css_sel = 'li.accessible-nav-dropdown:nth-child(1) > a:nth-child(1)'
    dash_a = browser.find_element_by_css_selector(dash_a_css_sel)
    print(dash_a.get_attribute('href'))
    assert 'dashboard' in dash_a.get_attribute('href')
    # + via new URL: timing critical still...
    browser.implicitly_wait(STD_WAIT_SECONDS)
    print(f'\nDEBUG: current_url: {browser.current_url}')
    assert 'dashboard' in browser.current_url

def verify_user_login(browser, user_key, username, pswd):
    """ Log in as specified user, in provided browser. """
    print(f'\nDEBUG: Logging in as "{username}"')
    # find login button
    login_button = browser.find_element(By.CLASS_NAME, 'btn-login')
    login_button.send_keys(Keys.RETURN)
    browser.implicitly_wait(STD_WAIT_SECONDS)
    # enter user details
    email_textbox = browser.find_element(By.ID, 'email')
    email_textbox.send_keys(username + Keys.TAB)
    crd_textbox = browser.find_element(By.ID, 'password')
    crd_textbox.send_keys(pswd + Keys.RETURN)
    # verify user logged in or not
    browser.implicitly_wait(STD_WAIT_SECONDS)
    if 'invalid' in user_key:
        verify_invalid_login(browser)
    else:
        verify_valid_login(browser)

def interact_with_cookies_banner(browser, accept=True):
    """ Accept or reject cookies: per user's choice. """
    print(f'\nDEBUG: Interacting with Cookies Banner: Accept: {accept}')
    if accept:
        cookie_accept_btn = browser.find_element(
            By.CLASS_NAME, 'btn-accept-cookie-banner'
        )
        cookie_accept_btn.click()

def get_json_from_file(filepath, encoding='UTF-8'):
    """ Returns JSON object|Dict from filepath """
    with open(filepath, 'r', encoding=encoding) as json_file:
        json_from_file = json.load(json_file)
    return json_from_file

def get_user_credentials(username, env_config):
    """ Return email and pswd of specified user, as a tuple. """
    user_email = env_config.get(username).get('email')
    user_pswd = env_config.get(username).get('pswd')
    return (user_email, user_pswd)

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
    browser_obj = None
    try:
        browser_obj = get_supported_browser(browser)
    finally:
        if browser_obj:
            browser_obj.close()

unsupported_browsers = ['safari', 'opera', 'ie']
@pytest.mark.parametrize('browser', unsupported_browsers)
def test_get_supported_browser_negative(browser):
    print(f'\nDEBUG: Browser under Test: unsupported: {browser.capitalize()}')
    with pytest.raises(UnsupportedBrowserException):
        get_supported_browser(browser)

def run_selenium_ui_verification_basics(browser_name, env_user_config, user):
    """ Execute basic web UI user actions, using Selenium WebDriver. """
    browser = None
    try:
        browser = get_supported_browser(browser_name)
        browser.get(URL)
        user_email, user_pswd = get_user_credentials(user, env_user_config)
        print(f'\nDEBUG: user: {user}, email: {user_email}')
        interact_with_cookies_banner(browser, accept=True)
        verify_user_login(browser, user, user_email, user_pswd)
    except SESSION_EXCEPTIONS as exc:
        print('\nDEBUG: Exception observed... Details: See below...')
        pprint(exc)
    finally:
        print(f'\nDEBUG: {browser_name}: Closing browser...')
        if browser:
            browser.close()
        print('Thank you.\n')


def main():
    """ Selenium Experiments: multiple browser support """
    for browser in SUPPORTED_BROWSERS:
        print(f'\nDEBUG: Browser: {browser.capitalize()}')
        env_user_config = get_json_from_file(ENV_CONFIG_FILE)
        userlist = env_user_config.keys()
        for user in userlist:
            run_selenium_ui_verification_basics(browser, env_user_config, user)


if __name__ == '__main__':
    main()
