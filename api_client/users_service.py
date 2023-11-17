import json
from json import JSONDecodeError

from api_client.api_client import ApiClient


class UsersService(ApiClient):
    def __init__(self, context):
        super(UsersService, self).__init__(self)
        self.context = context
        self.account_address = self.context.config_env.account_address
        self.chain_id = self.context.config_env.chain_id

        self.dispatcher = {
            'get': self.get,
            'post': self.post,
            'put': self.put,
            'delete': self.delete
        }

    def get_user_info(self, wallet_address=None, auth_token=None):
        request_url = '/users/v1/user'
        headers = {
            "authorization": f'Bearer {self.context.access_token if auth_token is None else auth_token }',
            "X-Chain-Id": '54211'
        }
        data = {
            "wallet_address": self.account_address if wallet_address is None else wallet_address
        }

        response = self.post(request_url, data=json.dumps(data), headers=headers)
        try:
            return {'response': json.loads(response.text), 'status_code': response.status_code}
        except JSONDecodeError:
            return {'response': response.text, 'status_code': response.status_code}

    def get_user_local_info(self, method='get', auth_token=None):
        request_url = '/users/v1/user/locale'
        headers = {
            "authorization": f'Bearer {self.context.access_token if auth_token is None else auth_token }',
            "x-chain-id": '54211'
        }
        response = self.dispatcher[method](endpoint=request_url, headers=headers)
        try:
            return {'response': json.loads(response.text), 'status_code': response.status_code}
        except JSONDecodeError:
            return {'response': response.text, 'status_code': response.status_code}

    def put_user_local_info(self, method='put', locale='en', auth_token=None):
        request_url = '/users/v1/user/locale'
        headers = {
            "authorization": f'Bearer {self.context.access_token if auth_token is None else auth_token }'
        }
        data = {
            "locale": locale
        }
        response = self.dispatcher[method](endpoint=request_url, data=json.dumps(data), headers=headers)
        try:
            return {'response': json.loads(response.text), 'status_code': response.status_code}
        except JSONDecodeError:
            return {'response': response.text, 'status_code': response.status_code}
