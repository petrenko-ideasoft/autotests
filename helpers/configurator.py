import os
import yaml

__config_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config')

config_path = os.path.join(__config_folder_path, 'config.local.yml' if 'config.local.yml' in os.listdir(
    __config_folder_path) else 'config.yml')


def get_config():
    with open(os.path.join(config_path), 'r') as ymlfile:
        return yaml.load(ymlfile, yaml.FullLoader)


class Configurator(object):
    _config = get_config()

    def __init__(self):
        super(Configurator, self)
        self.base_url = os.environ.get('BASE_URL', self._config.get('base_url'))
        self.account_address = os.environ.get('ACCOUNT_ADDRESS', self._config.get('account_address'))
        self.private_key = self._config.get('private_key')
        self.chain_id = self._config.get('chain_id')
        self.user_email_def = self._config.get('user_email_def')
        self.user_email_alt = self._config.get('user_email_alt')
