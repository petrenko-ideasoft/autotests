import json

from secrets import choice
from behave import *
from helpers.general_utils import GeneralUtils as GU


@step('send GET request to "{base_url}/backend/v1/version"')
def step_impl(context, base_url):
    context.step.name = context.step.name.format(base_url=context.base_url)
    context.response = context.client.info_service.get_backend_version()
    context.step.text = f'Response: {json.dumps(context.response["response"])}'


@step('send GET request to "{base_url}/auth/v1/version"')
def step_impl(context, base_url):
    context.step.name = context.step.name.format(base_url=context.base_url)
    context.response = context.client.info_service.get_auth_version()
    context.step.text = f'Response: {json.dumps(context.response["response"])}'


@step('send GET request to "{base_url}/email/v1/version"')
def step_impl(context, base_url):
    context.step.name = context.step.name.format(base_url=context.base_url)
    context.response = context.client.info_service.get_email_version()
    context.step.text = f'Response: {json.dumps(context.response["response"])}'


@step('send GET request to "{base_url}/users/v1/version"')
def step_impl(context, base_url):
    context.step.name = context.step.name.format(base_url=context.base_url)
    context.response = context.client.info_service.get_users_version()
    context.step.text = f'Response: {json.dumps(context.response["response"])}'
