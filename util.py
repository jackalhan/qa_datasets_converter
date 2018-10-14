import json

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
            '(function {}) is run successfuly and write the file: {}'.format(load_json_file.__name__, file_path))
    except Exception as e:
        logging.error('(function {}) has an error: {}'.format(load_json_file.__name__, e))
        raise