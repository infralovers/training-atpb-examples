from behave import when, given, then
import requests
import json

@given(u'I have a healthy API')
def step_impl(context):
    route = context.route.path_to("api_health_check")
    response = requests.get(route)
    assert response.status_code == 200
    data = json.loads(response.text)
    assert data['status'] == 'Ok'


@when(u'I create an article with the title "{title}"')
def step_impl(context, title):
    route = context.route.path_to("api_article_create")
    context.global_res = requests.post(
        route, json={"title": title, "content": "My article text"})

@when(u'I create an article with the title "{title}" and content "{content}')
def step_impl(context, title, content):
    route = context.route.path_to("api_article_create")
    context.global_res = requests.post(
        route, json={"title": title, "content": content})


@then(u'I should receive a "{resp}" response')
def step_impl(context, resp):
    if resp == 'success':
        status_code = 200
    else:
        status_code = 500
    assert context.global_res.status_code == status_code


@then(u'I should receive "{content}" in the response body')
def step_impl(context, content):
    assert content in context.global_res.text


@when(u'I list all available articles')
def step_impl(context):
    route = context.route.path_to("api_article_list")
    context.global_res = requests.get(route)
    print(context.global_res.status_code)
