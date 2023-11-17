import json
from helpers.general_utils import GeneralUtils as gu
from MaildropccReader import MaildropccReader

from behave import *


@step('send GET request to "{base_url}/users/v1/user"')
def step_impl(context, base_url):
    context.response = context.client.users_service.get_user_info()
    context.step.text = f'Response: {json.dumps(context.response["response"])}'


@given('send GET request to "{base_url}/users/v1/user" with invalid "{wallet}" wallet')
def step_impl(context, base_url, wallet):
    if 'random' in wallet:
        wallet = f'0x{gu.id_generator(40)}'
        context.step.name = context.step.name.replace('{random}', wallet)

    # context.step.name = context.step.name.replace('{base_url}', context.base_url)
    context.response = context.client.users_service.get_user_info(wallet_address=wallet)
    context.step.text = f'Response: {json.dumps(context.response["response"])}'


@given('post "{email}" email for user using ""{base_url}/users/v1/user/email"')
def step_impl(context, email, base_url):
    context.step.name = context.step.name.replace('{base_url}', context.base_url)


@given('send {method} request to "{base_url}/users/v1/user/locale"')
def step_impl(context, method, base_url):
    context.response = context.client.users_service.get_user_local_info(method=method.lower())


@given('send {method} request to "{base_url}/users/v1/user/locale" with "{locale}" locale')
def step_impl(context, method, base_url, locale):
    context.response = context.client.users_service.put_user_local_info(method=method.lower(), locale=locale)
