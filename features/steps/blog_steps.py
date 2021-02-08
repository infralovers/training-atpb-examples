from behave import when, given, then

@given(u'I am on "{page_name}"')
def step_impl(context, page_name):
    route = context.route.path_to(page_name)
    context.browser.get(route)
    context.browser.save_screenshot(page_name +".png")

@when(u'I follow "{link_text}"')
def step_impl(context, link_text):
    link = context.browser.find_element_by_link_text(link_text)
    assert link != None, "Was not able to find %s" % link_text
    print("link url: {}".format(link.get_attribute("href")))
    ## as link.click() does not work always on headless:
    # link.click()
    ## there are workarounds "available":
    # context.browser.execute_script("arguments[0].click();", link)
    context.browser.get(link.get_attribute("href"))

@then(u'I should be on "{page_name}"')
def step_impl(context, page_name):
    route = context.route.path_to(page_name)
    print(context.browser.current_url)
    print(route)
    assert context.browser.current_url == route


@then(u'I should see "{content}"')
def step_impl(context, content):
    assert content in context.browser.page_source
