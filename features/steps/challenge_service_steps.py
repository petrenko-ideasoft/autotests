import json
from behave import *
from helpers.general_utils import GeneralUtils


@given('send {method} request to "{base_url}/auth/v1/challenge/login"')
def step_impl(context, method, base_url):
    context.response = context.client.auth_service.challenge_login(method.lower())
    context.step.text = f'Response: {json.dumps(context.response["response"])}'


@given('send GET request to "{base_url}/auth/v1/challenge/login" with invalid "{wallet_address}" wallet address')
def step_impl(context, base_url, wallet_address):
    if 'invalid' in wallet_address:
        wallet_address = GeneralUtils.id_generator(42)
        context.step.name = context.step.name.replace('{invalid}', wallet_address)
    context.step.name = context.step.name.replace('{base_url}', context.base_url)
    context.response = context.client.auth_service.challenge_login(wallet_address=wallet_address)
