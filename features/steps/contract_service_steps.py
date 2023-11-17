from behave import *


@given('send {method} request to "{base_url}/backend/v1/contracts/created/of/user/list"')
def step_impl(context, method, base_url):
    context.response = context.client.contract_service.post_contracts_created_user_list(method.lower())


@given('send {method} request to "{base_url}/backend/v1/{contact}/info/for/deploy"')
def step_impl(context, method, base_url, contact):
    context.response = context.client.contract_service.get_info_about_contract(method=method.lower(),
                                                                               contract=contact)
