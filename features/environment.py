"""
behave environment configuration
"""
import os
import random
import threading
import tempfile
from wsgiref import simple_server
from wsgiref.simple_server import WSGIRequestHandler
import behave_webdriver
from behave import fixture, use_fixture
from paths import NavigationHelpers
from app import app
from headless_environment import get_headless_driver
DRIVER = os.getenv('DRIVER', 'firefox')

def get_firefox_driver():
    """get behave webdriver for firefox

    Returns:
        selenium webdriver
    """
    return behave_webdriver.Firefox.headless()


def get_browser_driver():
    """
    get a browser based in global DRIVER variables - defaults to firefox
    returns:
        a selenium webdriver
    """
    if DRIVER == "headless":
        return get_headless_driver()

    return get_firefox_driver()



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

    context.port = random.randint(5000, 5500)
    context.server = simple_server.WSGIServer(("0.0.0.0", context.port), WSGIRequestHandler)
    context.server.set_app(app)
    context.pa_app = threading.Thread(target=context.server.serve_forever)
    context.pa_app.start()

    context.route = NavigationHelpers(base_url=("http://127.0.0.1:%d" % context.port))
    context.browser = get_browser_driver()
    context.browser.set_page_load_timeout(10)


def after_all(context):
    """
    after testing the webdriver and webserver are closed and shutdown
    """
    context.browser.close()
    context.server.shutdown()
    context.pa_app.join()
