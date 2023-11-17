from behave import then


# @step('validate response by "{schema_name}" schema')
# def step_impl(context, schema_name):
#     service = schema_name.replace('get_', '')
#     service = service.replace('post_', '')
#     if isinstance(context.scenario_data[service]['response']['data'], list):
#         result = context.client.general_utils.verify_schema(schema_name,
#                                                             context.scenario_data[service]['response']['data'][0])
#     else:
#         result = context.client.general_utils.verify_schema(schema_name,
#                                                             context.scenario_data[service]['response']['data'])
#     assert result['validation'], f'Response data does not correspond to "{schema_name}" schema:\n{result["report_log"]}'


@then('validate response by "{schema_name}" schema')
def step_impl(context, schema_name):
    if len(context.response['response']) > 0:
        response = context.response['response']
        result = context.client.general_utils.verify_schema(schema_name, response)
        assert result['validation'], f'Response data does not correspond to "{schema_name}" schema:\n{result["report_log"]}'


@then("assert response code is {response_code:d}")
def step_impl(context, response_code):
    assert context.response['status_code'] == response_code, \
        f'Not appropriate response code\nExpected: {response_code}\nActual: {context.response["status_code"]}'


@then('reason "{message}" message presence in response')
def step_impl(context, message):
    assert context.response['response']['message'] == message, \
        f'Invalid response message\nExpected: {message}\nActual: {context.response["response"]["message"]}'
