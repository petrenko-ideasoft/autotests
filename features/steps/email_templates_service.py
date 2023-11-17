import json
from behave import *


@step('get languages list of templates by "{base_url}/email/v1/template/languages/list"')
def step_impl(context, base_url):
    context.step.name = context.step.name.format(base_url=context.base_url)
    context.response = context.client.email_service.get_template_languages_list()
    # context.test_data['review_id'] = context.response['response'].get('review_id')
    context.step.text = f'Response: {json.dumps(context.response["response"])}'


@given('post a new email template "{base_url}/email/v1/template"')
def step_impl(context, base_url):
    context.response = context.client.email_service.create_email_template()
    context.step.text = f'Response: {json.dumps(context.response["response"])}'


@given('post a new email template "{base_url}/email/v1//v1/template" with invalid authorization "{auth_token}" token')
def step_impl(context, base_url, auth_token):
    context.step.name = context.step.name.format(base_url=context.base_url)
    context.response = context.client.email_service.create_email_template(auth_token=auth_token)


@given(
    'get languages list of templates for "{language}" language by "{base_url}/email/v1/template/{language_type}/list" with invalid authorization "{auth_token}" token')
def step_impl(context, language, base_url, language_type, auth_token):
    context.step.name = context.step.name.format(base_url=context.base_url)
    context.response = context.client.email_service.get_email_templates_by_language(language=language,
                                                                                    auth_token=auth_token)

@given(
    'get languages list of templates for "{language}" language by "{base_url}/email/v1/template/{language_type}/list"')
def step_impl(context, language, base_url, language_type):
    context.step.name = context.step.name.format(base_url=context.base_url)
    context.response = context.client.email_service.get_email_templates_by_language(language)


@step('get info email template using "{base_url}/email/v1/template/{template_id}" by ID')
def step_impl(context, base_url, template_id):
    context.step.name = context.step.name.replace('{base_url}', context.base_url)
    if 'template_id' in template_id:
        template_id = context.response['response']['template_id']
        context.step.name = context.step.name.replace('{template_id}', template_id)

    context.response = context.client.email_service.get_email_templates_by_id(template_id)
    context.step.text = f'Response: {json.dumps(context.response["response"])}'


@step('update email template using "{base_url}/email/v1/template/{template_id}" by ID')
def step_impl(context, base_url, template_id):
    context.step.name = context.step.name.replace('{base_url}', context.base_url)
    if 'template_id' in template_id:
        template_id = context.response['response']['template_id']
        context.step.name = context.step.name.replace('{template_id}', template_id)

    context.response = context.client.email_service.update_email_template(template_id)
    context.step.text = f'Response: {json.dumps(context.response["response"])}'


@given('post a new email template "{base_url}/email/v1/template" with next data')
def step_impl(context, base_url):
    data = json.loads(context.step.text)
    context.step.name = context.step.name.format(base_url=context.base_url)
    context.response = context.client.email_service.create_email_template(data=data)
    context.step.text = context.step.text + '\n-----\n' + f'Response: {json.dumps(context.response["response"])}'


@step('get email template list by "{template_name}" name using "{base_url}/email/v1/template/by/name/list"')
def step_impl(context, template_name, base_url):
    context.step.name = context.step.name.replace('{base_url}', context.base_url)
    if 'template_name' in template_name:
        template_name = context.client.email_service.get_email_templates_by_id(
            context.response['response']['template_id'])['response']['name']
        context.step.name = context.step.name.replace('{template_name}', template_name)

    elif template_name == 'blank':
        template_name = ''

    context.step.name = context.step.name.replace('{template_name}', template_name)
    context.response = context.client.email_service.get_email_template_list_by_name(data={'name': template_name})
    context.step.text = f'Response: {json.dumps(context.response["response"])}'


@step('get email template list by with {limit} limit using "{base_url}/email/v1/template/by/name/list"')
def step_impl(context, limit, base_url):
    context.step.name = context.step.name.replace('{base_url}', context.base_url)
    template_name = context.client.email_service.get_email_templates_by_id(
        context.response['response']['template_id'])['response']['name']

    context.step.name = context.step.name.replace('{template_name}', template_name)
    context.response = context.client.email_service.get_email_template_list_by_name(data={'name': template_name,
                                                                                          'limit': limit})
    context.step.text = f'Response: {json.dumps(context.response["response"])}'


@step('post a new email template with the same name using "{base_url}/email/v1/template"')
def step_impl(context, base_url):
    context.step.name = context.step.name.replace('{base_url}', context.base_url)
    template_info = context.client.email_service.get_email_templates_by_id(
        context.response['response']['template_id'])['response']
    context.step.text = f'Template info: {json.dumps(template_info)}'

    context.response = context.client.email_service.create_email_template(data={'name': template_info['name']})
    context.step.text = context.step.text + '\n-----\n' + f'Response: {json.dumps(context.response["response"])}'


@step(
    'clone email "{template_id}" template for "{language}" language using "{base_url}/email/v1/template/clone/{source_template_id}/to/{target_language}/lang"')
def step_impl(context, template_id, language, base_url, source_template_id, target_language):
    if 'template_id' in template_id:
        template_id = context.response['response']['template_id']
        context.step.name = context.step.name.replace('{template_id}', template_id)
        context.step.name = context.step.name.replace('{source_template_id}', template_id)
    context.response = context.client.email_service.clone_template(template_id, language)

