import json
from time import sleep

import requests


class MailDropServer(object):
    def __init__(self, email_account):
        self.mail_server = 'https://api.maildrop.cc/v2/mailbox/'
        self.email_account = email_account.split("@")[0] if "@" in email_account else email_account
        self.json_headers = {
            'content-type': 'application/json',
        }
        self.session = requests.session()

    def get(self, endpoint, data=None, params=None, headers=None):
        return self.session.get(url=self.mail_server + endpoint, data=data, params=params,
                                headers=self.json_headers if headers is None else headers)

    def check_inbox(self):
        x_api_key = 'QM8VTHrLR2JloKTJMZ3N6Qa93FVsx8LapKCzEjui'
        self.json_headers.update({"x-api-key": x_api_key})
        response = self.get(endpoint=self.email_account, headers=self.json_headers)
        return json.loads(response.text)

    def read_email(self, email_account, email_id):
        response = self.get(endpoint=f'{email_account}/{email_id}', headers=self.json_headers)
        return json.loads(response.text)

    def get_code_from_email(self, user_email):
        response = self.check_inbox()
        for i in range(10):
            if len(response['messages']) > 0:
                email_id = response['messages'][0]['id']
                break
            else:
                sleep(20)
                response = self.check_inbox()
        email = self.read_email(self.email_account, email_id)
        return email['html'].split(':')[1]
