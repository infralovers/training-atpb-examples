@given(u'I am on "{page_name}"')
def step_impl(context, page_name):
    route = context.route.path_to(page_name)
    context.browser.get(route)

@when(u'I follow "About"')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I follow "About"')


@then(u'I should be on "the about page"')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I should be on "the about page"')


@then(u'I should see "About me"')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I should see "About me"')

