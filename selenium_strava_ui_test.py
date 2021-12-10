#!/usr/bin/python

"""
Web UI Test Automation Experiments: Selenium
"""

# pylint: disable=missing-function-docstring

import sys
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from msedge.selenium_tools import Edge, EdgeOptions

URL = 'https://www.strava.com'
USERNAME = 'me.bishanga@gmail.com'
CRD = 'foobar1234'
STD_WAIT_SECONDS = 20
MAL_EXIT_CODE = 1

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
    print(f'\nDEBUG: Interacting with Cookies Banner: Accept: {accept}')
    # if accept: click on appropriate button.
    if accept:
        cookie_accept_btn = browser.find_element(By.CLASS_NAME, 'btn-accept-cookie-banner')
        cookie_accept_btn.click()

def run_selenium_py_website_basics(browser_name):
    """ Do basic Web UI Actions, using Selenium WebDriver. """
    browser = get_supported_browser(browser_name)
    browser.get(URL)
    try:
        login_as_subscriber(browser, USERNAME, CRD)
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
    if name.lower() == 'microsoft':
        options = EdgeOptions()
        options.use_chromium = True
        return Edge(options=options)
    print(f"Unsupported browser: {name}")
    sys.exit(MAL_EXIT_CODE)

def main():
    """ StartingPoint: Selenium Experiments """
    ok_browser_names = ['firefox', 'chrome', 'microsoft']
    for browser in ok_browser_names:
        print(f'\nDEBUG: Browser: {browser.capitalize()}')
        run_selenium_py_website_basics(browser)


if __name__ == '__main__':
    main()
