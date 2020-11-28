#!usr/bin/python

# Web UI Test Automation Example: from Paul Knight.
# https://blog.testproject.io/2019/07/16/web-test-using-selenium-webdriver-python-chrome/

import os 
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def web_ui_auto_selenium_basics(browser_name):
    URL = 'https://www.strava.com'
    USERNAME = 'me.bishanga@gmail.com'
    CRD = 'abc1234'
    
    browser = get_supported_browser(browser_name)
    browser.get(URL)
    
    # login & verify
    login_button = browser.find_element_by_xpath('/html/body/div[2]/header/div/nav/a')
    login_button.send_keys(Keys.RETURN)
    
    # wait for login inputs frame to load.
    browser.implicitly_wait(20)

    email_textbox = browser.find_elements_by_id('email')[0]
    print('email_textbox:'); pprint(email_textbox)
    email_textbox.send_keys(USERNAME + Keys.TAB)

    crd_textbox = browser.find_elements_by_id('password')[0]
    print('cred_textbox: '); pprint(crd_textbox)
    crd_textbox.send_keys(CRD + Keys.RETURN)
    print('Thank you.\n')

    # select an event & verify

def get_supported_browser(name):
    if name.lower() == 'chrome':
        return webdriver.Chrome()
    elif name.lower() == 'firefox':
        return webdriver.Firefox()
    elif name.lower() == 'microsoft':
        return webdriver.Edge()
    else:
        print("unsupported browser: {}".format(name))
        exit(1)

test_browser_names = ['chrome', 'firefox', 'abc', 123]
for name in test_browser_names:
    web_ui_auto_selenium_basics(name)
