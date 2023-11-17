import json

from helpers.general_utils import GeneralUtils as gu
from json import JSONDecodeError
from api_client.api_client import ApiClient


class EmailService(ApiClient):
    def __init__(self, context):
        super(EmailService, self).__init__(self)
        self.context = context
        self.account_address = self.context.config_env.account_address

    def get_template_languages_list(self, auth_token=None):
        request_url = '/email/v1/template/languages/list'
        headers = {
            "authorization": f'Bearer {self.context.access_token if auth_token is None else auth_token }'
        }

        response = self.get(request_url, headers=headers if auth_token is None else auth_token)
        try:
            return {'response': json.loads(response.text), 'status_code': response.status_code}
        except JSONDecodeError:
            return {'response': response.text, 'status_code': response.status_code}

    def create_email_template(self, data=None, auth_token=None):
        if data is None:
            data = {}
        headers = {
            "authorization": f'Bearer {self.context.access_token if auth_token is None else auth_token}',
        }

        data = {
            "name": data.get('name', f'test_name_{gu.id_generator(10)}'),
            "subject": data.get("subject", "test_subject"),
            "language": data.get("language", "en"),
            "html": data.get('html', f'test_html_{gu.id_generator(50)}'),
            "plain": data.get('html', f'test_plain_{gu.id_generator(50)}')
        }
        request_url = '/email/v1/template'
        response = self.post(request_url, data=json.dumps(data), headers=headers)
        try:
            return {'response': json.loads(response.text), 'status_code': response.status_code}
        except JSONDecodeError:
            return {'response': response.text, 'status_code': response.status_code}

    def update_email_template(self, template_id, data=None, auth_token=None):
        if data is None:
            data = {}
        headers = {
            "authorization": f'Bearer {self.context.access_token if auth_token is None else auth_token}'
        }

        data = {
            "name": data.get('name', f'test_name_{gu.id_generator(10)}'),
            "subject": data.get("subject", "test_subject"),
            "language": data.get("language", "en"),
            "html": data.get('html', f'test_html_{gu.id_generator(50)}'),
            "plain": data.get('html', f'test_plain_{gu.id_generator(50)}')
        }
        request_url = f'/email/v1/template/{template_id}'
        response = self.post(request_url, data=json.dumps(data),
                             headers=headers)
        try:
            return {'response': json.loads(response.text), 'status_code': response.status_code}
        except JSONDecodeError:
            return {'response': response.text, 'status_code': response.status_code}

    def get_email_templates_by_language(self, language, limit=100, offset=100, auth_token=None):
        headers = {
            "authorization": f'Bearer {self.context.access_token if auth_token is None else auth_token }'
        }

        request_url = f'/email/v1/template/{language}/list?limit={limit}&offset={offset}'
        response = self.get(request_url, headers=headers)
        try:
            return {'response': json.loads(response.text), 'status_code': response.status_code}
        except JSONDecodeError:
            return {'response': response.text, 'status_code': response.status_code}

    def get_email_templates_by_id(self, template_id, auth_token=None):
        headers = {
            "authorization": f'Bearer {self.context.access_token if auth_token is None else auth_token}'
        }

        request_url = f'/email/v1/template/{template_id}'
        response = self.get(request_url, headers=headers)
        try:
            return {'response': json.loads(response.text), 'status_code': response.status_code}
        except JSONDecodeError:
            return {'response': response.text, 'status_code': response.status_code}

    def get_email_template_list_by_name(self, data=None, auth_token=None):
        if data is None:
            data = {}
        headers = {
            "authorization": f'Bearer {self.context.access_token if auth_token is None else auth_token}'
        }

        data = {
            "limit": data.get('limit', '1000'),
            "offset": data.get("offset", "1000"),
            "name": data.get("name", "")
        }
        request_url = f'/email/v1/template/by/name/list'
        response = self.post(request_url, data=json.dumps(data), headers=headers)
        try:
            return {'response': json.loads(response.text), 'status_code': response.status_code}
        except JSONDecodeError:
            return {'response': response.text, 'status_code': response.status_code}

    def clone_template(self, template_id, language, auth_token=None):
        headers = {
            "authorization": f'Bearer {self.context.access_token if auth_token is None else auth_token}'
        }

        request_url = f'/email/v1/template/clone/{template_id}/to/{language}/lang'
        response = self.get(request_url, headers=headers)
        try:
            return {'response': json.loads(response.text), 'status_code': response.status_code}
        except JSONDecodeError:
            return {'response': response.text, 'status_code': response.status_code}