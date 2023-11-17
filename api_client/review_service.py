import json
import os

from json import JSONDecodeError

from api_client.api_client import ApiClient


class ReviewService(ApiClient):
    def __init__(self, context):
        super(ReviewService, self).__init__(self)
        self.context = context
        self.account_address = self.context.config_env.account_address
        self.dispatcher = {
            'get': self.get,
            'post': self.post,
            'put': self.put,
            'delete': self.delete
        }

    def post_nft_id(self, request_data=None, method='post'):
        request_url = '/backend/v1/minting/nft/review'
        headers = {
            "authorization": f'Bearer {self.context.access_token}',
            "x-chain-id": '54211',
            "x-locale": "en"
        }
        if request_data is None:
            data = {}
        else:
            f = open(f'requests_data/{request_data}.json', "r")
            data = json.loads(f.read())
            f.close()
        self.context.step.text = f'Request data:\n{data}\n-----\n'

        response = self.dispatcher[method](endpoint=request_url, data=json.dumps(data), headers=headers)
        try:
            return {'response': json.loads(response.text), 'status_code': response.status_code}
        except JSONDecodeError:
            return {'response': response.text, 'status_code': response.status_code}

    def update_nft_review(self, review_id, method='put'):
        request_url = f'/backend/v1/minting/nft/review/{review_id}'
        headers = {
            "authorization": f'Bearer {self.context.access_token}',
            "x-chain-id": '54211',
            "x-locale": "en"
        }
        data = {
            "contract_address": "erc1155",
            "token_uri": "ipfs://bafkreidkaxflhvnmlfc6wqzwo2no37vexbmlqlto4w7sjidynxi4qhhxdi",
            "eip721_signature": "0xb5e6917cabb422034962140dfcf8bae72c9c6893b5a94ec33b3f84e875445eeb236e78db2208e1f01f822c992a71d5d849e030b85148677fb83f5b56a6393e461c",
            "royalty_percent": "0",
            "number_of_copies": "1",
            "comment": "Lorem Ipsum automation test"
        }

        response = self.dispatcher[method](endpoint=request_url, data=json.dumps(data), headers=headers)
        try:
            return {'response': json.loads(response.text), 'status_code': response.status_code}
        except JSONDecodeError:
            return {'response': response.text, 'status_code': response.status_code}

    def prepare_challenge_nft(self):
        request_url = '/backend/v1/review/nft/prepare/challenge'
        headers = {
            "authorization": f'Bearer {self.context.access_token}'
        }
        response = self.get(request_url, headers=headers)
        self.context.step.text = request_url

        try:
            return {'response': json.loads(response.text), 'status_code': response.status_code}
        except JSONDecodeError:
            return {'response': response.text, 'status_code': response.status_code}

    def generate_review_nft_token_id(self, review_id, contract_type):
        headers = {
            "authorization": f'Bearer {self.context.access_token}'
        }
        response = self.get(f'/backend/v1/review/nft/id/{review_id}/address/{contract_type}/token/id',
                            headers=headers)
        return {'response': json.loads(response.text), 'status_code': response.status_code}

    def create_review_nft_by_id(self, contract_type, review_id=None, contract_address=None, token_id=None):
        headers = {
            "authorization": f'Bearer {self.context.access_token}'
        }
        data = {
            "review_id": self.context.test_data['review_id'] if review_id is None else review_id,
            "erc_contract_type": contract_type,
            "image": "ipfs://bafybeiemxf5abjwjbikoz4mc3a3dla6ual3jsgpdr4cjr3oz3evfyavhwq",
            "name": "Automation NFT",
            "description": "This NFT created by automation",
            "number_of_copies": "1",
            "royalties": {"0x7F9eF291D1C3add01c96557961E22f13dD55cbD3": 10},
            "contract_address": self.context.test_data[
                'contract_address'] if contract_address is None else contract_address,
            "token_id": self.context.test_data['token_id'] if token_id is None else token_id,
            "metadata_json": [{"test-1": "qwerty1234"}],
            "comment": "Hello from automation."
        }

        response = self.post('/backend/v1/review/nft', data=json.dumps(data), headers=headers)
        return {'response': json.loads(response.text), 'status_code': response.status_code}

    def get_review_nft_by_id(self, review_id, method='get'):
        headers = {
            "authorization": f'Bearer {self.context.access_token}'
        }

        response = self.dispatcher[method](f'/backend/v1/review/request/{review_id}', headers=headers)
        try:
            return {'response': json.loads(response.text), 'status_code': response.status_code}
        except JSONDecodeError:
            return {'response': response.text, 'status_code': response.status_code}

    def get_list_with_review_requests(self, data=None, method='post'):
        headers = {
            "authorization": f'Bearer {self.context.access_token}'
        }
        if data is None:
            data = {}
        else:
            f = open(f'requests_data/{data}.json', "r")
            data = json.loads(f.read())
            f.close()
        self.context.step.text = f'Request data:\n{data}\n-----\n'
        response = self.dispatcher[method](f'/backend/v1/review/request/list', data=json.dumps(data), headers=headers)
        try:
            return {'response': json.loads(response.text), 'status_code': response.status_code}
        except JSONDecodeError:
            return {'response': response.text, 'status_code': response.status_code}

    def get_list_nft_listing_fixed_price(self, data=None, method='post', chain_id=None):
        headers = {
            "authorization": f'Bearer {self.context.access_token}'
        }
        if data is None:
            data = {}
        else:
            f = open(f'requests_data/{data}.json', "r")
            data = json.loads(f.read())
            f.close()
        self.context.step.text = f'Request data:\n{data}\n-----\n'
        response = self.dispatcher[method](f'/backend/v1/nft/{chain_id}/listing/fixed-price/list', data=json.dumps(data), headers=headers)
        try:
            return {'response': json.loads(response.text), 'status_code': response.status_code}
        except JSONDecodeError:
            return {'response': response.text, 'status_code': response.status_code}

    def get_nft_statistic(self, method='post', data=None, chain_id=None):
        if data is None:
            data = {}
        else:
            f = open(f'requests_data/{data}.json', "r")
            data = json.loads(f.read())
            f.close()
        self.context.step.text = f'Request data:\n{data}\n-----\n'
        response = self.dispatcher[method](f'/backend/v1/nft/{chain_id}/statistics', data=json.dumps(data))
        try:
            return {'response': json.loads(response.text), 'status_code': response.status_code}
        except JSONDecodeError:
            return {'response': response.text, 'status_code': response.status_code}

    def get_nft_whitelist(self, method='post', data=None, chain_id=None):
        if data is None:
            data = {}
        else:
            f = open(f'requests_data/{data}.json', "r")
            data = json.loads(f.read())
            f.close()
        self.context.step.text = f'Request data:\n{data}\n-----\n'
        response = self.dispatcher[method](f'/backend/v1/nft/{chain_id}/whitelist', data=json.dumps(data))
        try:
            return {'response': json.loads(response.text), 'status_code': response.status_code}
        except JSONDecodeError:
            return {'response': response.text, 'status_code': response.status_code}

    def get_nft_info(self, chain_id, contract_address, nft_id, method='get'):
        response = self.dispatcher[method](f'/backend/v1/nft/{chain_id}/{contract_address}/{nft_id}/info')
        try:
            return {'response': json.loads(response.text), 'status_code': response.status_code}
        except JSONDecodeError:
            return {'response': response.text, 'status_code': response.status_code}

    def renew_reviewed_nft_id(self, review_nft_id, account_address):
        request_url = f'/backend/v1/review/nft/id/{review_nft_id}/address/{account_address}/renewed'
        response = self.get(request_url)
        try:
            return {'response': json.loads(response.text), 'status_code': response.status_code}
        except JSONDecodeError:
            return {'response': response.text, 'status_code': response.status_code}

    def create_review_task_message(self, review_nft_id=None, account_address=None):
        data = {
            "review_nft_id": self.context.nft_id if review_nft_id is None else review_nft_id,
            "review_message": "Test description",
            "account_address": self.account_address if account_address is None else account_address
        }

        response = self.post('/backend/v1/review/nft/message', data=json.dumps(data))
        return {'response': json.loads(response.text), 'status_code': response.status_code}

    def request_review_messages_list(self, review_id, data=None, method='post'):
        headers = {
            "authorization": f'Bearer {self.context.access_token}'
        }
        if data is None:
            data = {}
        else:
            f = open(f'requests_data/{data}.json', "r")
            data = json.loads(f.read())
            f.close()
        self.context.step.text = f'Request data:\n{data}\n-----\n'

        response = self.dispatcher[method](f'/backend/v1/review/request/{review_id}/messages/list',
                                           data=json.dumps(data), headers=headers)
        try:
            return {'response': json.loads(response.text), 'status_code': response.status_code}
        except JSONDecodeError:
            return {'response': response.text, 'status_code': response.status_code}
