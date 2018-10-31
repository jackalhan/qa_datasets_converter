import logging
import argparse
import util as UTIL
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ds_formatter import qangaroo, mctest, insuranceqa, triviaqa, wikiqa, narrativeqa

def get_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('--log_path',help="path to the log file")
    parser.add_argument('--log_info',default="INFO", help="logging level")
    parser.add_argument('--source_file_path', help="path to the source file to be converted")
    parser.add_argument('--additional_source_files', help="addition/supporting files that are in the same path as source, could be coma-seperated ',', file type can be also identified with ':'. Ex: 'voc:vocabulary.txt, 'answer:answer.txt'")
    parser.add_argument('--source_dataset_format', help="dataset name of the source format")
    parser.add_argument('--destination_file_path', help="path to the destination file")
    parser.add_argument('--destination_dataset_format', help="dataset name of the destination format")
    return parser

def main(args):
    try:
        logging.info('(function {}) Started'.format(main.__name__))
        # TODO: 1) We need to create a interface class to have the same signature for all the formatters in ds_formatter folder.
        # TODO: 2) We need to create a generic approach to convert any type to any type not only any type to squad.
        # TODO: 3) can we have better approach to handle the following if/else scenarios
        # TODO: 4) we may also put some kind of field wrapper to handle whether which fields are gonna be filled with dummy and which fields are gonna be filled with real values.
        if args.source_dataset_format.lower() == 'qangaroo' and args.destination_dataset_format.lower() == 'squad' :
            in_content = UTIL.load_json_file(args.source_file_path, logging)
            formatted_content = qangaroo.convert_to_squad(in_content)
            UTIL.dump_json_file(args.destination_file_path, formatted_content, logging)
        elif args.source_dataset_format.lower() == 'mctest' and args.destination_dataset_format.lower() == 'squad':
            additional_files = UTIL.parse_additional_files(args.source_file_path, args.additional_source_files, logging)
            story_question_content = UTIL.load_csv_file(args.source_file_path,"\t", None, logging)
            answer_content = UTIL.load_csv_file(additional_files['answer'], "\t", None, logging)
            formatted_content = mctest.convert_to_squad(story_question_content, answer_content)
            UTIL.dump_json_file(args.destination_file_path, formatted_content, logging)
        elif args.source_dataset_format.lower() == 'insuranceqa' and args.destination_dataset_format.lower() == 'squad':
            additional_files = UTIL.parse_additional_files(args.source_file_path, args.additional_source_files, logging)
            voc = insuranceqa.load_vocab(additional_files['voc'])
            questions, a_to_q_map = insuranceqa.load_questions(args.source_file_path, voc)
            answers = insuranceqa.load_answers(additional_files['answer'], voc)
            formatted_content = insuranceqa.convert_to_squad(questions, answers, a_to_q_map)
            UTIL.dump_json_file(args.destination_file_path, formatted_content, logging)
        elif args.source_dataset_format.lower() == 'triviaqa' and args.destination_dataset_format.lower() == 'squad':
            additional_files = UTIL.parse_additional_files(args.source_file_path, args.additional_source_files, logging)
            wiki = additional_files['wikipedia']
            web = additional_files['web']
            seed = additional_files['seed']
            max_num_of_tokens = additional_files['max_num_of_tokens']
            sample_size = additional_files['sample_size']
            qa_file = UTIL.load_json_file(args.source_file_path)
            formatted_content = triviaqa.convert_to_squad_format(qa_file, args.destination_file_path, wiki, web, sample_size, seed, max_num_of_tokens)
            UTIL.dump_json_file(args.destination_file_path, formatted_content, logging)
        elif args.source_dataset_format.lower() == 'wikiqa' and args.destination_dataset_format.lower() == 'squad':
            story_question_content = UTIL.load_csv_file(args.source_file_path, "\t", 'infer', logging)
            formatted_content = wikiqa.convert_to_squad(story_question_content)
            UTIL.dump_json_file(args.destination_file_path, formatted_content, logging)
        elif args.source_dataset_format.lower() == 'narrativeqa' and args.destination_dataset_format.lower() == 'squad':
            additional_files = UTIL.parse_additional_files(args.source_file_path, args.additional_source_files, logging)
            story_summary_content = UTIL.load_csv_file(args.source_file_path, ",", 'infer', logging)
            question_content = UTIL.load_csv_file(additional_files['qaps'], ",", 'infer', logging)
            set_type = additional_files['set']
            formatted_content = narrativeqa.convert_to_squad(story_summary_content, question_content, set_type)
            UTIL.dump_json_file(args.destination_file_path, formatted_content, logging)
        elif args.source_dataset_format.lower() == 'webqa' and args.destination_dataset_format.lower() == 'squad':
            additional_files = UTIL.parse_additional_files(args.source_file_path, args.additional_source_files, logging)
            story_summary_content = UTIL.load_csv_file(args.source_file_path, ",", 'infer', logging)
            question_content = UTIL.load_csv_file(additional_files['qaps'], ",", 'infer', logging)
            set_type = additional_files['set']
            formatted_content = narrativeqa.convert_to_squad(story_summary_content, question_content, set_type)
            UTIL.dump_json_file(args.destination_file_path, formatted_content, logging)
        else:
            pass
        logging.info('(function {}) Finished'.format(main.__name__))
    except Exception as e:
        logging.error('(function {}) has an error: {}'.format(main.__name__, e))
        raise
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