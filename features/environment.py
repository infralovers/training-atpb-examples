"""
behave environment configuration
"""
import os
import random
import threading
import tempfile
from wsgiref import simple_server
from selenium import webdriver
from behave import fixture, use_fixture
from paths import NavigationHelpers
from app import app

DRIVER = os.getenv('DRIVER', 'firefox')
SELENIUM_API = os.getenv('SELENIUM', 'http://127.0.0.1:4444/wd/hub')

def get_headless_driver():
    """get headless behave webdriver for chrome

    Returns:
        selenium webdriver
    """
    firefox_options = webdriver.FirefoxOptions()
    return webdriver.Remote(
        command_executor=SELENIUM_API,
        options=firefox_options
    )

def get_firefox_driver():
    """get behave webdriver for firefox

    Returns:
        selenium webdriver
    """
    options = webdriver.FirefoxOptions()
    options.headless = True
    return webdriver.Firefox(options=options)

select_browser = {
    "firefox": get_firefox_driver,
    "headless": get_headless_driver
}

def get_browser_driver():
    """
    get a browser based in global DRIVER variables - defaults to firefox
    returns:
        a selenium webdriver
    """
    driver = select_browser.get(DRIVER)()
    driver.set_window_size(1920, 1080)
    driver.set_page_load_timeout(10)
    return driver


# pylint: disable=W0613
@fixture
def fixture_database_setup(context, *args, **kwargs):
    """
    fix application client setup with a temporary database, which is destroyed after the test
    The unsued argument warning is explicit deactivated,
    because the fixure method requires those parameters,
    but those parameters are not used within the current implementation
    """
    db_file, app.config['DATABASE'] = tempfile.mkstemp()
    app.testing = True
    context.client = app.test_client()
    yield context.client

    # cleanup after getting back to this code:
    os.close(db_file)
    os.unlink(app.config['DATABASE'])


def before_all(context):
    """
    before all tests are started a setup for the test context is needed:
        - run http server
        - setup navigation helpers
        - setup selenium webdriver
    """
    use_fixture(fixture_database_setup, context)

    context.port = random.randint(5000, 5500)
    context.server = simple_server.WSGIServer(("0.0.0.0", context.port), \
                                               simple_server.WSGIRequestHandler)
    context.server.set_app(app)
    context.pa_app = threading.Thread(target=context.server.serve_forever)
    context.pa_app.start()

    context.route = NavigationHelpers(base_url=("http://127.0.0.1:%d" % context.port))
    context.browser = get_browser_driver()


def after_all(context):
    """
    after testing the webdriver and webserver are closed and shutdown
    """
    context.browser.close()
    context.server.shutdown()
    context.pa_app.join()
