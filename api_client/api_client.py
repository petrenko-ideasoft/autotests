import requests
import os

from helpers.configurator import Configurator


class ApiClient(object):
    def __init__(self, context):
        self.config = Configurator()
        self.context = context
        self.server = self.config.base_url
        self.json_headers = {
            'content-type': 'application/json',
            'accept': '*/*'
        }
        self.session = requests.session()
        self.info = None

    def get(self, endpoint, data=None, params=None, headers=None):
        return self.session.get(url=self.server + endpoint, data=data, params=params,
                                headers=self.json_headers if headers is None else headers)

    def post(self, endpoint, data=None, params=None, headers=None):
        return self.session.post(url=self.server + endpoint, data=data, params=params,
                                 headers=self.json_headers if not headers else headers)

    def delete(self, endpoint, data=None, params=None, headers=None):
        return self.session.delete(url=self.server + endpoint, data=data, params=params,
                                   headers=self.json_headers if not headers else headers)

    def patch(self, endpoint, data=None, params=None, headers=None):
        return self.session.patch(url=self.server + endpoint, data=data, params=params,
                                  headers=self.json_headers if not headers else headers)

    def put(self, endpoint, data=None, params=None, headers=None):
        return self.session.put(url=self.server + endpoint, data=data, params=params,
                                headers=self.json_headers if not headers else headers)

    def clear_cookies(self):
        self.session.cookies.clear()