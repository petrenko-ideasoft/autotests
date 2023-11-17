import datetime
import json

from json import JSONDecodeError

from api_client.api_client import ApiClient


class ContractService(ApiClient):
    def __init__(self, context):
        super(ContractService, self).__init__(self)
        self.context = context
        self.account_address = self.context.config_env.account_address
        self.dispatcher = {
            'get': self.get,
            'post': self.post,
            'put': self.put,
            'delete': self.delete
        }

    def post_contracts_created_user_list(self, method='post', access_token=None):
        request_url = '/backend/v1/contracts/created/of/user/list'
        headers = {
            "authorization": f'Bearer {self.context.access_token if access_token is None else access_token}',
            "x-chain-id": self.context.config_env.chain_id
        }
        data = {
            "pagination": {
                "direction": "next",
                "per_page": "10",
                "cursor": {
                    "contract_address": self.context.config_env.account_address,
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
                }
            },
            "sorting": "asc",
            "order_by": "contract_address",
            "filter": [
                {
                    "relation": "and",
                    "data_field": "contract_address",
                    "condition": "contains",
                    "value": "0x10C7adA39"
                }
            ]
        }

        response = self.dispatcher[method](endpoint=request_url, data=json.dumps(data), headers=headers)
        try:
            return {'response': json.loads(response.text), 'status_code': response.status_code}
        except JSONDecodeError:
            return {'response': response.text, 'status_code': response.status_code}

    def get_info_about_contract(self, contract, method='post', access_token=None):
        request_url = f'/backend/v1/{contract}/info/for/deploy'
        headers = {
            "authorization": f'Bearer {self.context.access_token if access_token is None else access_token}',
            "x-chain-id": self.context.config_env.chain_id
        }

        response = self.dispatcher[method](endpoint=request_url, headers=headers)
        try:
            return {'response': json.loads(response.text), 'status_code': response.status_code}
        except JSONDecodeError:
            return {'response': response.text, 'status_code': response.status_code}