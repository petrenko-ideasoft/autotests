import json

from behave import *
from helpers.general_utils import GeneralUtils


@given('send GET request to "{base_url}/auth/v1/auth/login/check"')
def step_impl(context, base_url):
    context.response = context.client.auth_service.auth_login_check()
    context.step.text = f'Response: {json.dumps(context.response["response"])}'


@given('send GET request to "{base_url}/auth/v1/auth/login/check" with invalid "{access_token}" access token')
def step_impl(context, base_url, access_token):
    if 'invalid' in access_token:
        access_token = GeneralUtils.id_generator(42)
        context.step.name = context.step.name.replace('{invalid}', access_token)
    context.response = context.client.auth_service.auth_login_check(access_token)
    context.step.text = f'Response: {json.dumps(context.response["response"])}'


@given('send {method} request to "{base_url}/auth/v1/auth/login/renewed"')
def step_impl(context, method, base_url):
    context.response = context.client.auth_service.renew_login(method.lower())
    context.step.text = f'Response: {json.dumps(context.response["response"])}'


@given('send {method} request to "​{base_url}/auth/v1​/auth​/login" with Etherum signature')
def step_impl(context, method, base_url):
    data = context.response
    context.response = context.client.auth_service.auth_login(hmac=data['hmac'],
                                                              challenge_value=data['challenge_value'],
                                                              signature=data['signature'])
    context.step.text = f'Response: {json.dumps(context.response["response"])}'


@given("get Etherum signature")
def step_impl(context):
    context.response = context.client.auth_service.get_ethereum_signature()
    context.step.text = f'Response: {json.dumps(context.response)}'
