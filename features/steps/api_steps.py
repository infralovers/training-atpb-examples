import requests
import json


@given(u'I have a healthy API')
def step_impl(context):
    route = context.route.path_to("api_health_check")
    response = requests.get(route)
    assert response.status_code == 200
    data = json.loads(response.text)
    assert data['status'] == 'Ok'


@when(u'I create an article with the title "{string}"')
def step_impl(context, string):
    context.global_res = requests.post(
        "http://localhost:5000/api/article", json={"title": string, "content": "My article text"})

@then(u'I should receive a "{string}" response')
def step_impl(context, string):
    if string == 'success':
        status_code = 200
    else:
        status_code = 500

    assert context.global_res.status_code == status_code


@then(u'I should receive "{string}" in the response body')
def step_impl(context, string):
    assert string in context.global_res.text

@when(u'I list all available articles')
def step_impl(context):
    context.global_res = requests.get("http://localhost:5000/api/article")
    print(context.global_res.status_code)
