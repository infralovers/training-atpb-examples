from behave import when, given, then
from selenium.webdriver.common.by import By

@given(u'I am on "{page_name}"')
def step_impl(context, page_name):
    route = context.route.path_to(page_name)
    context.browser.get(route)

@when(u'I follow "{link_text}"')
def step_impl(context, link_text):
    link = context.browser.find_element(By.LINK_TEXT, link_text)
    link.click()

@then(u'I should be on "{page_name}"')
def step_impl(context, page_name):
    route = context.route.path_to(page_name)
    assert context.browser.current_url == route

@then(u'I should see "{content}"')
def step_impl(context, content):
    assert content in context.browser.page_source
