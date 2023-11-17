import json
import os
import fauxfactory

from random import randint
from faker import Faker
from jsonschema import Draft7Validator, validate
from jsondiff import diff

fake = Faker(['en_GB'])


def read_schema(schema_name):
    schema_folder_path = os.path.abspath('schemas')
    schema_path = os.path.join(schema_folder_path, f'{schema_name}.json')

    with open(schema_path) as json_file:
        schema = json.load(json_file)
    return schema


class GeneralUtils(object):
    @staticmethod
    def id_generator(size=8, utf8=False):
        if utf8:
            alphasize = randint(1, size - 1)
            utfsize = size - alphasize
            result = fauxfactory.gen_alphanumeric(alphasize) + fauxfactory.gen_utf8(utfsize)
        else:
            result = fauxfactory.gen_alphanumeric(size)
        return result

    @staticmethod
    def fake_text(chars_num=200):
        return fake.text(max_nb_chars=chars_num).replace('\n', ' ')

    @staticmethod
    def verify_schema(schema_name, to_validate):
        """
        Verifies all schema properties
        """
        schema = read_schema(schema_name)

        v = Draft7Validator(schema)
        errors = sorted(v.iter_errors(to_validate), key=lambda e: e.path)
        validated = True
        report_log = None
        if len(errors) > 0:
            errors_list = []
            for err in errors:
                path_list = []
                for i in err.path:
                    path_list.append(f'[{i}]')
                path = f" for \"{''.join(path_list)}\" property"
                errors_list.append(f'* {err.message}{path if len(path_list) > 0 else ""}'.replace("'", '"'))
            report_log = '\n'.join(errors_list)
            validated = False
        return {'validation': validated, 'report_log': report_log}

    @staticmethod
    def validate_schema_properties(properties, schema):
        """
        Verifies specified properties
        properties: takes a dictionary of properties
        example: {"property1": value, "property2": value}
        """
        # validate({"1": "spam", 2: "eggs"}, schema)
        return validate(properties, schema)

    @staticmethod
    def get_absolute_file_path(folder, file_name):
        schema_folder_path = os.path.abspath(folder)
        return os.path.join(schema_folder_path, file_name)

    @staticmethod
    def read_table_column(table, column_order=0):
        v_table = []
        for i in table:
            v_table.append(i[column_order])
        return v_table

    @staticmethod
    def read_json_file(folder, file_name):
        json_folder_path = os.path.abspath(folder)
        json_path = os.path.join(json_folder_path, f'{file_name}.json')

        with open(json_path) as json_file:
            data = json.load(json_file)
        return data

    @staticmethod
    def write_json_file(folder, file_name, data):
        json_folder_path = os.path.abspath(folder)
        json_path = os.path.join(json_folder_path, f'{file_name}.json')

        with open(json_path, 'w') as f:
            json.dump(data, f, indent=2)

    @staticmethod
    def compare_properties_values(expected, actual, output='text'):
        response = json.loads(diff(actual, expected, dump=True))
        if '$delete' in response:
            ignored = response.pop('$delete')
        if len(response) > 0:
            if output == 'file':
                file_name = f'error_{GeneralUtils.id_generator()}.txt'
                with open(f'tmp/{file_name}', 'w') as outfile:
                    json.dump(response, outfile, indent=2)
                return {'status': False, 'result': file_name}
            elif output == 'text':
                return {'status': False, 'result': json.dumps(response)[1:-1]} if len(response) > 0 else {'status': True}
        else:
            return {'status': True}

    @staticmethod
    def change_value_in_json(file, folder, key, new_value):
        data = GeneralUtils.read_json_file(folder, file)
        for item in data['data']:
            if item in key:
                data['data'][key] = new_value

        GeneralUtils.write_json_file('tmp/', file, data)

    @staticmethod
    def get_index_number(dict, criteria_key):
        for i in dict:
            if i[0] == criteria_key:
                item_index = dict.index(i)
                break
        return item_index

    @staticmethod
    def to_bool(value):
        if str(value).lower() in ("yes", "y", "true", "t", "1"): return True
        if str(value).lower() in ("no", "n", "false", "f", "0", "0.0", "", "none", "[]", "{}"): return False
        raise Exception('Invalid value for boolean conversion: ' + str(value))
