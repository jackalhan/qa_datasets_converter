import json
import pandas as pd
import os
def load_json_file(file_path, logging):
    content = None
    try:
        with open(file_path, 'r') as f_in:
            content = json.load(f_in)
        logging.info('(function {}) is run successfuly and load the file: {}'.format(load_json_file.__name__, file_path))
    except Exception as e:
        logging.error('(function {}) has an error: {}'.format(load_json_file.__name__, e))
        raise
    return content

def dump_json_file(file_path, content, logging):
    try:
        with open(file_path, 'w') as f_out:
            json.dump(content, f_out, indent=1)

        logging.info(
            '(function {}) is run successfuly and write the file: {}'.format(dump_json_file.__name__, file_path))
    except Exception as e:
        logging.error('(function {}) has an error: {}'.format(dump_json_file.__name__, e))
        raise

def load_csv_file(file_path, sep, header, logging):
    content = None
    try:
        with open(file_path, 'r') as f_in:
            content = pd.read_csv("/home/jackalhan/Downloads/mc160.dev.ans.txt",sep=sep, header=header)
        logging.info(
            '(function {}) is run successfuly and load the file: {}'.format(load_csv_file.__name__, file_path))
    except Exception as e:
        logging.error('(function {}) has an error: {}'.format(load_csv_file.__name__, e))
        raise
    return content

def parse_additional_files(file_path, additional_files, logging, seperator=','):
    source_path = file_path.rpartition(os.sep)[0]
    _additional_files = []
    try:
        for _ in additional_files.split(seperator):
            if not os.path.isfile(_):
                _additional_files.append(os.path.join(source_path, _))
            else:
                _additional_files.append(_)
        logging.info(
            '(function {}) is run successfuly'.format(parse_additional_files.__name__, file_path))
    except Exception as e:
        logging.error('(function {}) has an error: {}'.format(parse_additional_files.__name__, e))
        raise
    return _additional_files