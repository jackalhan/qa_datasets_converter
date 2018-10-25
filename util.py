import json
import pandas as pd
import os
def load_json_file(file_path, logging, encoding='utf-8'):
    content = None
    try:
        # with open(file_path, 'r') as f_in:
        # content = json.load(f_in)
        content = json.loads(get_file_contents(file_path, encoding=encoding))
        if logging is not None:
            logging.info('(function {}) is run successfuly and load the file: {}'.format(load_json_file.__name__, file_path))
    except Exception as e:
        if logging is not None:
            logging.error('(function {}) has an error: {}'.format(load_json_file.__name__, e))
        raise
    return content

def dump_json_file(file_path, content, logging, encoding='utf-8'):
    try:
        with open(file_path, 'w', encoding=encoding) as f_out:
            json.dump(content, f_out, indent=1)
        if logging is not None:
            logging.info(
                '(function {}) is run successfuly and write the file: {}'.format(dump_json_file.__name__, file_path))
    except Exception as e:
        if logging is not None:
            logging.error('(function {}) has an error: {}'.format(dump_json_file.__name__, e))
        raise

# def write_json_to_file(json_object, json_file, mode='w', encoding='utf-8'):
#     with open(json_file, mode, encoding=encoding) as outfile:
#         json.dump(json_object, outfile, indent=4, sort_keys=True, ensure_ascii=False)


def get_file_contents(filename, encoding='utf-8'):
    with open(filename, encoding=encoding) as f:
        content = f.read()
    return content


def get_file_contents_as_list(file_path, encoding='utf-8', ignore_blanks=True):
    contents = get_file_contents(file_path, encoding=encoding)
    lines = contents.split('\n')
    lines = [line for line in lines if line != ''] if ignore_blanks else lines
    return lines

def load_csv_file(file_path, sep, header, logging):
    content = None
    try:
        with open(file_path, 'r') as f_in:
            content = pd.read_csv("/home/jackalhan/Downloads/mc160.dev.ans.txt",sep=sep, header=header)
        if logging is not None:
            logging.info(
                '(function {}) is run successfuly and load the file: {}'.format(load_csv_file.__name__, file_path))
    except Exception as e:
        if logging is not None:
            logging.error('(function {}) has an error: {}'.format(load_csv_file.__name__, e))
        raise
    return content

def parse_additional_files(file_path, additional_files, logging, item_seperator=',', k_v_seperator=':'):
    source_path = file_path.rpartition(os.sep)[0]
    _additional_files = dict()
    try:
        for _ in additional_files.split(item_seperator):
            _splitted = _.split(k_v_seperator)
            key = _splitted[0]
            value = _splitted[1]
            if not os.path.isfile(_):
                _additional_files[key] = os.path.join(source_path, value)
            else:
                _additional_files[key] = value
        if logging is not None:
            logging.info(
                '(function {}) is run successfuly'.format(parse_additional_files.__name__, file_path))
    except Exception as e:
        if logging is not None:
            logging.error('(function {}) has an error: {}'.format(parse_additional_files.__name__, e))
        raise
    return _additional_files