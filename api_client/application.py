from api_client.auth_service import AuthService
from api_client.info_service import InfoService
from api_client.email_service import EmailService
from api_client.review_service import ReviewService
from api_client.users_service import UsersService
from api_client.contracts_service import ContractService
from helpers.general_utils import GeneralUtils


class Application:
    def __init__(self, context):
        self.general_utils = GeneralUtils()
        self.info_service = InfoService(context)
        self.review_service = ReviewService(context)
        self.auth_service = AuthService(context)
        self.email_service = EmailService(context)
        self.users_service = UsersService(context)
        self.contract_service = ContractService(context)
