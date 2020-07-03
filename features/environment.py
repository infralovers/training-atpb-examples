import os
import threading
import tempfile
from wsgiref import simple_server
from wsgiref.simple_server import WSGIRequestHandler
import behave_webdriver
from selenium import webdriver
from behave import fixture, use_fixture
from paths import NavigationHelpers
from app import app, init_db

SELENIUM = os.getenv('SELENIUM', 'http://127.0.0.1:4444/wd/hub')
DRIVER = os.getenv('DRIVER', 'firefox')


def get_chrome_driver():
    browser = webdriver.Chrome()
    return browser


def get_firefox_driver():
    browser = webdriver.Firefox()
    return browser


def get_headless_driver(driver):
    return behave_webdriver.Chrome.headless()

def get_browser_driver():
    if DRIVER == "firefox":
        return get_firefox_driver()
    if DRIVER == "chrome":
        return get_chrome_driver()

    return get_headless_driver(DRIVER)


@fixture
def app_client(context, *args, **kwargs):
    context.db, app.config['DATABASE'] = tempfile.mkstemp()
    app.testing = True
    context.client = app.test_client()
    with app.app_context():
        init_db()

    yield context.client
    # -- CLEANUP:
    os.close(context.db)
    os.unlink(app.config['DATABASE'])


def before_all(context):

    use_fixture(app_client, context)

    context.server = simple_server.WSGIServer(("", 5000), WSGIRequestHandler)
    context.server.set_app(app)
    context.pa_app = threading.Thread(target=context.server.serve_forever)
    context.pa_app.start()

    context.route = NavigationHelpers()
    context.browser = get_browser_driver()
    context.browser.set_page_load_timeout(10)


def after_all(context):
    context.browser.close()
    context.server.shutdown()
    context.pa_app.join()
