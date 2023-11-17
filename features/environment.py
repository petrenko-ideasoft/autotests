import os
import configparser
import traceback

from mimetypes import guess_type

from api_client import api_client
from api_client.application import Application
from helpers.configurator import Configurator
from api_client.auth_service import AuthService
from time import time, sleep
# Report Portal versions >= 5.0.0:
from reportportal_client import ReportPortalService

rp_config = configparser.ConfigParser()
config_path = os.path.join('behave.local.ini')
if not os.path.exists(config_path):
    config_path = os.path.join('behave.ini')
rp_config.read(config_path)

endpoint = rp_config.get('report_portal', 'rp_endpoint')
project = rp_config.get('report_portal', 'rp_project')
token = rp_config.get('report_portal', 'rp_token')
launch_name = rp_config.get('report_portal', 'rp_launch_name')
launch_doc = rp_config.get('report_portal', 'rp_launch_description')


def timestamp():
    return str(int(time() * 1000))


def my_error_handler(exc_info):
    """
    This callback function will be called by async service client when error occurs.
    Return True if error is not critical and you want to continue work.
    :param exc_info: result of sys.exc_info() -> (type, value, traceback)
    :return:
    """
    print("Error occurred: {}".format(exc_info[1]))
    traceback.print_exception(*exc_info)


# Report Portal versions >= 5.0.0:
service = ReportPortalService(endpoint=endpoint, project=project, token=token)


def before_all(context):
    userdata = context.config.userdata

    context.launch = None
    context.config_env = Configurator()
    context.base_url = context.config_env.base_url

    context.client = Application(context)

    context.etherum_signature = context.client.auth_service.get_ethereum_signature()
    context.access_token = context.client.auth_service.auth_login(
        hmac=context.etherum_signature['hmac'], challenge_value=context.etherum_signature['challenge_value'],
        signature=context.etherum_signature['signature'])['response']['access_token']

    context.job_name = userdata.get('JOB_NAME', '%s run' % context.config.tags.ands[0][0] if len(
        context.config.tags.ands) > 0 else 'Test debug').replace('_', ' ').capitalize()
    branch_name = userdata.get('BRANCH', 'Not specified')

    context.build_name = userdata.get('BUILD_NAME', 'No build info provided')
    context.build_url = userdata.get('BUILD_URL', None)

    launcher_description = f'Server: {context.base_url}\nBranch: {branch_name}'

    context.launch = service.start_launch(name=f'{context.job_name} API tests',
                                          start_time=timestamp(),
                                          description=launcher_description,
                                          mode='DEBUG')
    context.garbage_wallets = []


def before_feature(context, feature):
    context.test_data = {}
    context.feature_id = service.start_test_item(name='Feature: %s' % feature.name,
                                                 description='Feature description: %s' % '\n'.join(feature.description),
                                                 start_time=timestamp(),
                                                 item_type="SUITE")


def before_scenario(context, scenario):
    # Start test item.
    if "skip" in scenario.effective_tags:
        service.start_test_item(name='Scenario: %s' % scenario.name,
                                description='Skipped due to %s' % scenario.description[0],
                                start_time=timestamp(),
                                item_type='SCENARIO',
                                parent_item_id=context.feature_id)

        service.log(time=timestamp(),
                    message='Skipped reason: %s' % scenario.description[0],
                    level='TRACE',
                    item_id=context.feature_id)
        scenario.skip()
    else:
        context.scenario_data = {}
        case_id = 'No test case ID specified' if len(scenario.description) == 0 else scenario.description[0]
        context.scenario_id = service.start_test_item(name='Scenario: %s' % scenario.name,
                                                      description=get_scenario_description(scenario),
                                                      start_time=timestamp(),
                                                      item_type="SCENARIO",
                                                      parent_item_id=context.feature_id)


def before_step(context, step):
    context.step = step
    if 'base_url' in context.step.name:
        context.step.name = context.step.name.replace('{base_url}', context.base_url)
    context.attach_response = {'attach': False}


def after_step(context, step):
    if step.status.name == 'passed':
        if step.table:
            result = format_table_data(step.table.rows)
            service.log(time=timestamp(),
                        message=f'{step.keyword} {step.name}\n~~~~~~~~~~~~~~~~~~~~~~~~~\nStep data table:\n{result}',
                        level='INFO',
                        item_id=context.scenario_id)
        elif step.text:
            service.log(time=timestamp(),
                        message=f'{step.keyword} {step.name}',
                        level='INFO',
                        item_id=context.scenario_id)
            service.log(time=timestamp(),
                        message=f'Step data text:\n{step.text}',
                        level='TRACE',
                        item_id=context.scenario_id)
        elif context.attach_response['attach']:
            service.log(time=timestamp(),
                        message=f'{step.keyword} {step.name}',
                        level='INFO',
                        item_id=context.scenario_id)
        else:
            service.log(time=timestamp(),
                        message=f'{step.keyword} {step.name}',
                        level='INFO',
                        item_id=context.scenario_id)
        if context.attach_response['attach']:
            attach_log_file(context)

    if step.status.name == 'failed':
        if step.table:
            result = format_table_data(step.table.rows)
            service.log(time=timestamp(),
                        message=f'{step.keyword} {step.name}\n~~~~~~~~~~~~~~~~~~~~~~~~~\nStep data table:\n{result}\n{"_" * (len(step.keyword + step.name) + 1)}\n{step.exception.args[0]}',
                        level='FATAL',
                        item_id=context.scenario_id)
        else:
            service.log(time=timestamp(),
                        message='%s %s\n%s\n%s' % (step.keyword, step.name, ("_" * (len(step.keyword + step.name) + 1)),
                                                   step.exception.args[0]),
                        level="FATAL",
                        item_id=context.scenario_id)
        if context.attach_response['attach']:
            attach_expected_values(context)


def after_scenario(context, scenario):
    try:
        del context.scenario_data
    except AttributeError:
        pass
    if scenario.status.name == 'failed':
        service.finish_test_item(end_time=timestamp(), status="FAILED", item_id=context.scenario_id)
    elif scenario.status.name == 'skipped':
        service.finish_test_item(end_time=timestamp(), status="SKIPPED", item_id=context.scenario_id)
    else:
        service.finish_test_item(end_time=timestamp(), status="PASSED", item_id=context.scenario_id)


def after_feature(context, feature):
    service.finish_test_item(end_time=timestamp(), status="PASSED", item_id=context.feature_id)


def after_all(context):
    for w in context.garbage_wallets:
        context.client.wallets.delete_wallet(wallet_currency=w['currency'], public_key=w['public_key'])
    # Finishes launcher.
    service.finish_launch(end_time=timestamp())
    service.terminate()


def get_scenario_description(scenario):
    try:
        return scenario.description[0]
    except (IndexError):
        return 'No scenario description'


def format_table_data(rows):
    table_data = []
    for row in rows:
        table_data.append(' | '.join(row))
    return "| %s |" % ' |\n| '.join(table_data)


def attach_log_file(context):
    context.attach_response['attach'] = False
    log_file = f'tmp/{context.attach_response["file_name"]}'
    with open(log_file, "rb") as fh:
        attachment = {
            "name": os.path.basename(log_file),
            "data": fh.read(),
            "mime": guess_type(log_file)[0] or "application/octet-stream"
        }
        service.log(time=timestamp(),
                    message='\nResponse body data >>>=====>',
                    level="TRACE",
                    item_id=context.scenario_id,
                    attachment=attachment,
                    )
        sleep(2)  # delay is required due to give a time to attach a file


def attach_expected_values(context):
    context.attach_response['attach'] = False
    log_file = f'tmp/{context.attach_response["file_name"]}'
    with open(log_file, "rb") as fh:
        attachment = {
            "name": os.path.basename(log_file),
            "data": fh.read(),
            "mime": guess_type(log_file)[0] or "application/octet-stream"
        }
        service.log(time=timestamp(),
                    message='Review expected values >>>=====>',
                    level="WARN",
                    item_id=context.scenario_id,
                    attachment=attachment,
                    )
        sleep(2)
