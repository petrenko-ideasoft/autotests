import datetime
import json
import re
from json import JSONDecodeError

from web3 import Web3, EthereumTesterProvider
from eth_account.messages import encode_defunct
from api_client.api_client import ApiClient


class AuthService(ApiClient):
    def __init__(self, context):
        super(AuthService, self).__init__(self)
        self.context = context
        self.base_url = self.context.config_env.base_url
        self.account_address = self.context.config_env.account_address
        self.dispatcher = {
            'get': self.get,
            'post': self.post,
            'put': self.put,
            'delete': self.delete
        }

    def get_ethereum_signature(self, wallet_address=None, private_key=None):
        response = self.challenge_login()['response']

        wallet_address = self.config.account_address if wallet_address is None else wallet_address
        chain_id = self.config.chain_id
        nonce = response['request_id'].replace('-', '')
        expiration = response['expires_on']
        url = re.compile(r"https?://(www\.)?")
        host = url.sub('', self.context.base_url).strip().strip('/')
        issued_at = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

        challenge_value = f'{host} wants you to sign in with your Ethereum account:\n{wallet_address}\n\nSign In {host}\n\nURI: {self.context.base_url}\nVersion: 1\nChain ID: {chain_id}\nNonce: {nonce}\nIssued At: {issued_at}\nExpiration Time: {expiration}'
        w3 = Web3(EthereumTesterProvider())
        message = encode_defunct(text=challenge_value)

        signed_message = w3.eth.account.sign_message(
            message, private_key=self.context.config_env.private_key if private_key is None else private_key)
        return {'challenge_value': challenge_value,
                'hmac': response['hmac'],
                'signature': signed_message.signature.hex()}

    def auth_login(self, hmac, challenge_value, signature):
        data = {
            "challenge_value": challenge_value,
            "hmac": hmac,
            "signature": signature
        }
        response = self.post('/auth/v1/auth/login', data=json.dumps(data))

        return {'response': json.loads(response.text), 'status_code': response.status_code}

    def challenge_login(self, method='post', wallet_address=None):
        data = {
            "wallet_address": self.config.account_address if wallet_address is None else wallet_address,
            "sign_type": "eip4361"
        }

        response = self.dispatcher[method]('/auth/v1/challenge/login', data=json.dumps(data))
        try:
            self.context.step.text = (
                f'Request data:\n{json.dumps(data)}\n-----\nResponse data:\n{response.text}')
        except AttributeError:
            pass

        return {'response': json.loads(response.text), 'status_code': response.status_code}

    def auth_login_check(self, access_token=None):
        self.clear_cookies()
        headers = {
            "authorization": f'Bearer {self.context.access_token if access_token is None else access_token}'
        }
        response = self.get('/auth/v1/auth/login/check', headers=headers)

        return {'response': json.loads(response.text), 'status_code': response.status_code}

    def renew_login(self, method='get', access_token=None):
        headers = {
            "authorization": f'{self.context.access_token if access_token is None else access_token}'
        }
        response = self.dispatcher[method]('/auth/v1/auth/login/renewed', headers=headers)
        try:
            self.context.access_token = json.loads(response.text)['access_token']
        #     # return {'response': json.loads(response.text), 'status_code': response.status_code}
        except KeyError:
            pass
        # except JSONDecodeError:
        return {'response': json.loads(response.text), 'status_code': response.status_code}

    # return {'response': json.loads(response.text), 'status_code': response.status_code}
