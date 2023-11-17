import json
from json import JSONDecodeError

from api_client.api_client import ApiClient


class InfoService(ApiClient):
    def __init__(self, context):
        super(InfoService, self).__init__(self)
        self.context = context

    def get_backend_version(self):
        request_url = f'/backend/v1/version'
        response = self.get(request_url)
        try:
            return {'response': json.loads(response.text), 'status_code': response.status_code}
        except JSONDecodeError:
            return {'response': response.text, 'status_code': response.status_code}

    def get_auth_version(self):
        request_url = f'/auth/v1/version'
        response = self.get(request_url)
        try:
            return {'response': json.loads(response.text), 'status_code': response.status_code}
        except JSONDecodeError:
            return {'response': response.text, 'status_code': response.status_code}

    def get_email_version(self):
        request_url = f'/email/v1/version'
        response = self.get(request_url)
        try:
            return {'response': json.loads(response.text), 'status_code': response.status_code}
        except JSONDecodeError:
            return {'response': response.text, 'status_code': response.status_code}

    def get_users_version(self):
        request_url = f'/users/v1/version'
        response = self.get(request_url)
        try:
            return {'response': json.loads(response.text), 'status_code': response.status_code}
        except JSONDecodeError:
            return {'response': response.text, 'status_code': response.status_code}