import os
import threading
from wsgiref import simple_server
from wsgiref.simple_server import WSGIRequestHandler
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from app import app
from paths import NavigationHelpers
from models import Schema
from selenium.webdriver.common.keys import Keys

SELENIUM = os.getenv('SELENIUM', 'http://localhost:4444/wd/hub')
DRIVER = os.getenv('DRIVER', 'firefox')


def get_driver_capabilities():
    desired_capabilities = webdriver.DesiredCapabilities.FIREFOX
    desired_capabilities['loggingPrefs'] = {'browser': 'ALL'}
    return desired_capabilities


def get_firefox_driver():
    desired_capabilities = get_driver_capabilities()
    browser = webdriver.Firefox(desired_capabilities=desired_capabilities)
    return browser


def get_headless_driver():
    desired_capabilities = get_driver_capabilities()
    browser = webdriver.Remote(
        command_executor=SELENIUM,
        desired_capabilities=desired_capabilities)
    return browser

def get_browser_driver():
    if DRIVER == "firefox":
        return get_firefox_driver()
    return get_headless_driver()


def before_all(context):
    Schema()
    context.server = simple_server.WSGIServer(("", 5000), WSGIRequestHandler)
    context.server.set_app(app)
    context.pa_app = threading.Thread(target=context.server.serve_forever)
    context.pa_app.start()

    context.route = NavigationHelpers()

    context.browser = get_browser_driver()

    context.browser.set_page_load_timeout(time_to_wait=200)


def after_all(context):
    context.browser.quit()
    context.server.shutdown()
    context.pa_app.join()
