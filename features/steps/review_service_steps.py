from behave import *
import json

from helpers.general_utils import GeneralUtils


@given('send {method} request to "{base_url}/backend/v1/minting/nft/review" with "{request_data}" data')
def step_impl(context, method, base_url, request_data):
    context.response = context.client.review_service.post_nft_id(method=method.lower(), request_data=request_data)
    context.step.text = context.step.text + f'Response: {json.dumps(context.response["response"])}'


@given("get NFT ID")
def step_impl(context):
    context.nft_id = context.client.review_service.get_nft_id()['response']["review_id"]
    context.step.text = f'NFT ID: {context.nft_id}'


@step('post new NFT using "{base_url}/backend/v1/review/nft" with "{contract_type}" contract type')
def step_impl(context, base_url, contract_type):
    context.step.name = context.step.name.format(base_url=context.base_url)
    context.response = context.client.review_service.create_review_nft_by_id(contract_type)
    context.test_data['review_id'] = context.response['response'].get('review_id')
    context.step.text = f'Response: {json.dumps(context.response["response"])}'


@step('post new NFT using "{base_url}/v1/review/nft" with {nft_id} NFT ID')
def step_impl(context, base_url, nft_id):
    context.step.name = context.step.name.format(base_url=context.base_url)
    context.response = context.client.review_service.post_new_nft(nft_id)


@step('get renewed NFT ID using "{base_url}/backend/v1/review/nft/id/{review_id}/address/{account_address}/renewed"')
def step_impl(context, base_url, review_id, account_address):
    if 'review_id' in review_id:
        review_id = context.test_data['review_id']

    context.step.name = context.step.name.replace('{base_url}', context.base_url)
    context.step.name = context.step.name.replace('{review_id}', review_id)
    context.step.name = context.step.name.replace('{account_address}', context.config_env.account_address)

    context.response = context.client.review_service.renew_reviewed_nft_id(review_id,
                                                                           context.config_env.account_address)

    try:
        context.test_data['review_nft_id'] = context.response['response']['review_nft_id']
        context.step.text = f'Response: {json.dumps(context.response["response"])}'
    except KeyError:
        pass


@step('post a message of review task by {review_nft_id} using "{base_url}/backend/v1/review/nft/message"')
def step_impl(context, review_nft_id, base_url):
    if 'review_nft_id' in review_nft_id:
        review_nft_id = context.test_data['review_nft_id']
        context.step.name = context.step.name.replace('{review_nft_id}', review_nft_id)
    elif 'invalid' in review_nft_id:
        review_nft_id = GeneralUtils.id_generator(232)
        context.step.name = context.step.name.replace('{invalid}', review_nft_id)

    context.step.name = context.step.name.replace('{base_url}', context.base_url)

    context.response = context.client.review_service.create_review_task_message(review_nft_id)
    context.step.text = f'Response: {json.dumps(context.response["response"])}'


@given('send GET request to "{base_url}/backend/v1/review/nft/prepare/challenge"')
def step_impl(context, base_url):
    context.response = context.client.review_service.prepare_challenge_nft()
    context.step.text = f'Response: {json.dumps(context.response["response"])}'


@given("generate the review NFT ID")
def step_impl(context):
    context.response = context.client.review_service.post_nft_id()
    context.test_data['review_id'] = context.response['response']['review_id']
    context.step.text = f'Response: {json.dumps(context.response["response"])}'


@step(
    'generate review NFT token ID "{base_url}/backend/v1/review/nft/id/{review_id}/address/{contract_type}/token/id"')
def step_impl(context, base_url, review_id, contract_type):
    if 'review_id' in review_id:
        review_id = context.test_data['review_id']
        context.step.name = context.step.name.replace('{review_id}', review_id)

    context.response = context.client.review_service.generate_review_nft_token_id(review_id, contract_type)
    context.step.text = f'Response: {json.dumps(context.response["response"])}'


@step('generate review NFT token ID with "{contract_type}" contract type')
def step_impl(context, contract_type):
    response = context.client.review_service.generate_review_nft_token_id(context.test_data['review_id'],
                                                                          contract_type)
    context.test_data['contract_address'] = response['response']['contract_address']
    context.test_data['token_id'] = response['response']['token_id']
    context.step.text = f'Response: {json.dumps(response["response"])}'


@step('send {method} request to "{base_url}/backend/v1/review/request/{review_id}"')
def step_impl(context, method, base_url, review_id):
    if 'review_id' in review_id:
        review_id = context.response['response']['review_id']
        context.step.name = context.step.name.replace('{review_id}', review_id)
    context.response = context.client.review_service.get_review_nft_by_id(method=method.lower(), review_id=review_id)
    context.step.text = f'Response: {json.dumps(context.response["response"])}'


@step('send {method} request to "{base_url}/backend/v1/minting/nft/review/{review_id}"')
def step_impl(context, method, base_url, review_id):
    if 'review_id' in review_id:
        review_id = context.response['response']['review_id']
        context.step.name = context.step.name.replace('{review_id}', review_id)
    context.response = context.client.review_service.update_nft_review(method=method.lower(), review_id=review_id)


@given('send {method} request to "{base_url}/backend/v1/review/request/list" with "{request_data}" data')
def step_impl(context, method, base_url, request_data):
    context.response = context.client.review_service.get_list_with_review_requests(method=method.lower(),
                                                                                   data=request_data)
    context.step.text = context.step.text + f'Response: {context.response}'


@given(
    'send {method} request to "{base_url}/backend/v1/nft/{chain_id}/listing/fixed-price/list" with "{request_data}" data')
def step_impl(context, method, base_url, chain_id, request_data):
    if 'chain_id' in chain_id:
        chain_id = context.config_env.chain_id
        context.step.name = context.step.name.replace('{chain_id}', chain_id)
    context.response = context.client.review_service.get_list_nft_listing_fixed_price(
        method=method.lower(), data=request_data, chain_id=chain_id)
    context.step.text = context.step.text + f'Response: {context.response}'


@given('send {method} request to "{base_url}/backend/v1/nft/{chain_id}/statistics" with "{request_data}" data')
def step_impl(context, method, base_url, chain_id, request_data):
    if 'chain_id' in chain_id:
        chain_id = context.config_env.chain_id
        context.step.name = context.step.name.replace('{chain_id}', chain_id)
    context.response = context.client.review_service.get_nft_statistic(method=method.lower(), data=request_data,
                                                                       chain_id=chain_id)
    context.step.text = context.step.text + f'Response: {context.response}'


@given('send {method} request to "{base_url}/backend/v1/nft/{chain_id}/whitelist" with "{request_data}" data')
def step_impl(context, method, base_url, chain_id, request_data):
    if 'chain_id' in chain_id:
        chain_id = context.config_env.chain_id
        context.step.name = context.step.name.replace('{chain_id}', chain_id)
    context.response = context.client.review_service.get_nft_whitelist(method=method.lower(), data=request_data,
                                                                       chain_id=chain_id)
    context.step.text = context.step.text + f'Response: {context.response}'


@given('send {method} request to "{base_url}/backend/v1/nft/{chain_id}/{contract_address}/{nft_id}/info"')
def step_impl(context, method, base_url, chain_id, contract_address, nft_id):
    if 'chain_id' in chain_id:
        chain_id = context.config_env.chain_id
        context.step.name = context.step.name.replace('{chain_id}', chain_id)
    context.response = context.client.review_service.get_nft_info(method=method.lower(), chain_id=chain_id,
                                                                  contract_address=contract_address, nft_id=nft_id)
    context.step.text = f'Response: {context.response}'
