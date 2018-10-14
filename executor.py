import logging
import argparse
import util as UTIL
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ds_formatter import qangaroo

def get_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('--log_path',help="path to the log file")
    parser.add_argument('--log_info',default="INFO", help="logging level")
    parser.add_argument('--source_file_path', help="path to the source file to be converted")
    parser.add_argument('--source_dataset_format', help="dataset name of the source format")
    parser.add_argument('--destination_file_path', help="path to the destination file")
    parser.add_argument('--destination_dataset_format', help="dataset name of the destination format")
    return parser

def main(args):
    logging.info('(function {}) Started'.format(main.__name__))
    # TODO: 1) We need to create a interface to have the same signature for all the formatters in ds_formatter folder.
    # TODO: 2) We need to create a generic approach to convert any type to any type not only any type to squad.
    # TODO: 3) can we have better approach to handle the following if/else scenarios
    if args.source_dataset_format.lower() == 'qangaroo' and args.destination_dataset_format.lower() == 'squad' :
        in_content = UTIL.load_json_file(args.source_file_path, logging)
        out_content = qangaroo.convert_to_squad(in_content)
        UTIL.dump_json_file(args.destination_file_path, out_content, logging)
    logging.info('(function {}) Finished'.format(main.__name__))
if __name__ == '__main__':
    args = get_parser().parse_args()
    assert args.log_path is not None, "No log path found at {}".format(args.log_path)
    assert args.source_file_path is not None, "No source file path found at {}".format(args.source_file_path)
    assert args.source_dataset_format is not None, "No source_dataset_format found {}".format(args.source_dataset_format)
    assert args.destination_file_path is not None, "No destination file path found at {}".format(args.destination_file_path)
    assert args.destination_dataset_format is not None, "No destination dataset format found {}".format(
        args.destination_dataset_format)

    if args.log_info.lower() =='info':
        log_info = logging.INFO
    elif args.log_info.lower() == 'debug':
        log_info = logging.DEBUG
    elif args.log_info.lower() == 'warn':
        log_info = logging.WARNING
    elif args.log_info.lower() == 'critical':
        log_info = logging.CRITICAL
    elif args.log_info.lower() == 'error':
        log_info = logging.ERROR
    else:
        log_info = logging.INFO

    logging.basicConfig(filename=args.log_path, level=log_info)
    main(args)