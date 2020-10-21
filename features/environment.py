"""
behave environment configuration
"""
import os
import threading
import tempfile
from wsgiref import simple_server
from wsgiref.simple_server import WSGIRequestHandler
import behave_webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FFOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
from behave import fixture, use_fixture
from paths import NavigationHelpers
from app import app

SELENIUM = os.getenv('SELENIUM', 'http://127.0.0.1:4444/wd/hub')
DRIVER = os.getenv('DRIVER', 'firefox')


def get_chrome_driver():
    """get behave webdriver for chrome

    Returns:
        selenium webdriver
    """
    return behave_webdriver.Chrome.headless()


def get_firefox_driver():
    """get behave webdriver for firefox

    Returns:
        selenium webdriver
    """
    return behave_webdriver.Firefox.headless()


def get_headless_driver():
    """get headless behave webdriver for chrome

    Returns:
        selenium webdriver
    """

    chrome_options = ChromeOptions()
#    chrome_options.add_argument("--headless") # argument to set no sandBox
    chrome_options.add_argument("--no-sandbox") # argument to set no sandBox
    chrome_options.add_argument("--disable-setuid-sandbox") # and switch off suid sandBox
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--whitelisted-ips=localhost,127.0.0.1")
    chrome_options.add_argument("--verbose")
    desired_capabilities = chrome_options.to_capabilities()

    browser = webdriver.Remote(
        command_executor=SELENIUM,
        desired_capabilities=desired_capabilities)
    browser.implicitly_wait(5)

    return browser


def get_browser_driver():
    """
    get a browser based in global DRIVER variables - defaults to firefox
    returns:
        a selenium webdriver
    """
    if DRIVER == "firefox":
        return get_firefox_driver()
    if DRIVER == "chrome":
        return get_chrome_driver()

    return get_headless_driver()


# pylint: disable=W0613
@fixture
def app_client(context, *args, **kwargs):
    """
    fix application client setup with a temporary database, which is destroyed after the test
    The unsued argument warning is explicit deactivated,
    because the fixure method requires those parameters,
    but those parameters are not used within the current implementation
    """
    context.db, app.config['DATABASE'] = tempfile.mkstemp()
    app.testing = True
    context.client = app.test_client()
#    with app.app_context():
#        init_db()

    yield context.client
    # -- CLEANUP:
    os.close(context.db)
    os.unlink(app.config['DATABASE'])


def before_all(context):
    """
    before all tests are started a setup for the test context is needed:
        - run http server
        - setup navigation helpers
        - setup selenium webdriver
    """
    use_fixture(app_client, context)

    context.server = simple_server.WSGIServer(("0.0.0.0", 5000), WSGIRequestHandler)
    context.server.set_app(app)
    context.pa_app = threading.Thread(target=context.server.serve_forever)
    context.pa_app.start()

    context.route = NavigationHelpers()
    context.browser = get_browser_driver()
    context.browser.set_page_load_timeout(10)


def after_all(context):
    """
    after testing the webdriver and webserver are closed and shutdown
    """
    context.browser.close()
    context.server.shutdown()
    context.pa_app.join()
