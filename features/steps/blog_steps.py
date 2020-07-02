@given(u'I am on "{page_name}"')
def step_impl(context, page_name):
    route = context.route.path_to(page_name)
    context.browser.get(route)

@when(u'I follow "{string}"')
def step_impl(context,string):
    link = context.browser.find_element_by_link_text(string)
    link.click()

@then(u'I should be on "{page_name}"')
def step_impl(context, page_name):
    route = context.route.path_to(page_name)
    assert context.browser.current_url == route

@then(u'I should see "{string}"')
def step_impl(context,string):
   assert string in context.browser.page_source 
