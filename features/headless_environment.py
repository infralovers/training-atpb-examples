"""
behave headless environment configuration for cicd
"""

import os
from selenium import webdriver

SELENIUM = os.getenv('SELENIUM', 'http://127.0.0.1:4444/wd/hub')

def get_headless_driver():
    """get headless behave webdriver for chrome

    Returns:
        selenium webdriver
    """
    firefox_options = webdriver.FirefoxOptions()
    browser = webdriver.Remote(
        command_executor=SELENIUM,
        options=firefox_options
    )
    browser.implicitly_wait(5)

    return browser
