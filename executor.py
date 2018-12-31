import logging
import argparse
import util as UTIL
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ds_formatter import qangaroo, mctest, insuranceqa, triviaqa, wikiqa, narrativeqa, msmarco, ubuntudialogue, cnnnews, squad, quasar


def get_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('--log_path',help="path to the log file")
    parser.add_argument('--log_info',default="INFO", help="logging level")
    parser.add_argument('--data_path', help="path to the source file to be converted")
    parser.add_argument('--from_files', help="addition/supporting files that are in the same path as source, could be coma-seperated ',', file type can be also identified with ':'. Ex: 'voc:vocabulary.txt, 'answer:answer.txt'")
    parser.add_argument('--from_format', help="dataset name of the source format")
    parser.add_argument('--to_format', help="dataset name of the destination format")
    parser.add_argument('--to_file_name', help="destination file name")
    return parser

def main(args):
    try:
        logging.info('(function {}) Started'.format(main.__name__))

        source_files = UTIL.parse_source_files(args.data_path, args.from_files, logging)
        source_file = source_files['source']
        destination_file = os.path.join(args.data_path, args.from_format.lower() + '_to_' + args.to_format.lower() + '_'+args.to_file_name)

        # TODO: 1) We need to create a interface class to have the same signature for all the formatters in ds_formatter folder.
        # TODO: 2) We need to create a generic approach to convert any type to any type not only any type to squad.
        # TODO: 3) can we have better approach to handle the following if/else scenarios
        # TODO: 4) we may also put some kind of field wrapper to handle whether which fields are gonna be filled with dummy and which fields are gonna be filled with real values.
        if args.from_format.lower() == 'qangaroo' and args.to_format.lower() == 'squad' :
            """            
            --log_path="~/log.log" 
            --data_path="~/data/qangaroo_v1.1/wikihop" 
            --from_files="source:dev.json"
            --from_format="qangaroo" 
            --to_format="squad" 
            --to_file_name="dev.json" #it is gonna be renamed as "[from_to]_filename.what"
            """
            in_content = UTIL.load_json_file(source_file, logging)
            formatted_content = qangaroo.convert_to_squad(in_content)
            UTIL.dump_json_file(destination_file, formatted_content, logging)

        elif args.from_format.lower() == 'mctest' and args.to_format.lower() == 'squad':
            """            
            --log_path="~/log.log" 
            --data_path="~/data/" 
            --from_files="source:mc160.dev.tsv" 
            --from_format="mctest" 
            --to_format="squad" 
            --to_file_name="mc160.dev.json" #it is gonna be renamed as "[from_to]_filename.what"
            """


            story_question_content = UTIL.load_csv_file(source_file,"\t", None, logging)
            #answer_content = UTIL.load_csv_file(additional_files['answer'], "\t", None, logging)
            formatted_content = mctest.convert_to_squad(story_question_content)
            UTIL.dump_json_file(destination_file, formatted_content, logging)

        elif args.from_format.lower() == 'insuranceqa' and args.to_format.lower() == 'squad':
            """            
            --log_path="~/log.log" 
            --data_path="~/data/insuranceqa_v2" 
            --from_files="source:InsuranceQA.question.anslabel.token.1500.pool.solr.test.encoded,voc:vocabulary.txt,answer:InsuranceQA.label2answer.token.encoded"
            --from_format="insuranceqa" 
            --to_format="squad" 
            --to_file_name="1500.test.json"
            """

            voc = insuranceqa.load_vocab(source_files['voc'])
            questions, a_to_q_map = insuranceqa.load_questions(source_file, voc)
            answers = insuranceqa.load_answers(source_files['answer'], voc)
            formatted_content = insuranceqa.convert_to_squad(questions, answers, a_to_q_map)
            UTIL.dump_json_file(destination_file, formatted_content, logging)

        elif args.from_format.lower() == 'triviaqa' and args.to_format.lower() == 'squad':
            """            
            --log_path="~/log.log" 
            --data_path="~/data/triviaqa/" 
            --from_files=""source:qa/wikipedia-train.json, wikipedia:evidence/wikipedia,web:evidence/web,seed:10,token_size:2000,sample_size:1000000"
            --from_format="triviaqa" 
            --to_format="squad" 
            --to_file_name="wikipedia-train-long.json"
            """

            wiki = source_files['wikipedia']
            web = source_files['web']
            seed = source_files['seed']
            max_num_of_tokens = source_files['token_size']
            sample_size = source_files['sample_size']
            qa_file = UTIL.load_json_file(source_file, logging)
            formatted_content = triviaqa.convert_to_squad_format(qa_file, wiki, web, sample_size, seed, max_num_of_tokens)
            UTIL.dump_json_file(destination_file, formatted_content, logging)
        elif args.from_format.lower() == 'wikiqa' and args.to_format.lower() == 'squad':
            """            
            --log_path="~/log.log" 
            --data_path="~/data/WikiQACorpus" 
            --from_files="source:WikiQA-dev.tsv"
            --from_format="wikiqa" 
            --to_format="squad" 
            --to_file_name="dev.json"
            """

            story_question_content = UTIL.load_csv_file(source_file, "\t", 'infer', logging)
            formatted_content = wikiqa.convert_to_squad(story_question_content)
            UTIL.dump_json_file(destination_file, formatted_content, logging)

        elif args.from_format.lower() == 'squad' and args.to_format.lower() == 'matchzoo':
            """       
            **sample.txt**: Each line is the raw query and raw document text of a document. The format is "label \t query \t document_txt".     
            --log_path="~/log.log" 
            --data_path="~/data/squad" 
            --from_files="source:dev-v1.1.json,q_len:1000,negative_sampling:100"
            --from_format="squad" 
            --to_format="matchzoo" 
            --to_file_name="dev.txt"
            """
            negative_samp_count = int(source_files['negative_sampling'])
            q_len = int(source_files['q_len'])
            content = UTIL.load_json_file(source_file, logging)
            generator = squad.yield_to_matchzoo(content, q_len, negative_samp_count)
            open(destination_file, "w").write('\n'.join(data for data in generator))

            #UTIL.dump_json_file(destination_file, formatted_content, logging)
        elif args.from_format.lower() == 'squad' and args.to_format.lower() == 'lucene':
            """       
            **sample.txt**: Each line is the raw query and raw document text of a document. The format is "label \t query \t document_txt".     
            --log_path="~/log.log" 
            --data_path="~/data/squad" 
            --from_files="source:dev-v1.1.json,doc_type_verbose:2"
            --from_format="squad" 
            --to_format="matchzoo" 
            --to_file_name="dev.txt"
            """
            doc_type_verbose = int(source_files['doc_type_verbose'])
            content = UTIL.load_json_file(source_file, logging)
            squad.convert_to_lucene(content, doc_type_verbose, args.data_path)
        elif args.from_format.lower() == 'squad' and args.to_format.lower() == 'short_squad':
            """       
            **sample.txt**: Each line is the raw query and raw document text of a document. The format is "label \t query \t document_txt".     
            --log_path="~/log.log" 
            --data_path="~/data/squad" 
            --from_files="source:dev-v1.1.json,q_len:1000,negative_sampling:100"
            --from_format="squad" 
            --to_format="short_squad" 
            --to_file_name="dev.json"
            """
            negative_samp_count = int(source_files['negative_sampling'])
            q_len = int(source_files['q_len'])
            content = UTIL.load_json_file(source_file, logging)
            formatted_content = squad.convert_to_short_squad(content, q_len, negative_samp_count)
            UTIL.dump_json_file(destination_file, formatted_content, logging)
        elif args.from_format.lower() == 'squad' and args.to_format.lower() == 'squad':
            """       
               In order to make some analyzes.      
              --log_path="~/log.log" 
              --data_path="~/data/squad" 
              --from_files="source:dev-v1.1.json,is_histogram:True,document_type:1" #1 for question, #2 for paragraphs, #3 for both.
              --from_format="squad" 
              --to_format="squad" 
              --to_file_name="dev.json"
            """
            is_historgram = source_files['is_histogram']
            document_type = int(source_files['document_type'])
            his_bin = int(source_files['histogram_bin'])
            content = UTIL.load_json_file(source_file, logging)
            squad.print_statistics(content, is_historgram, his_bin, document_type)

        elif args.from_format.lower() == 'narrativeqa' and args.to_format.lower() == 'squad':
            """            
            --log_path="~/log.log" 
            --data_path="~/data/narrativeqa" 
            --from_files="source:summaries.csv,set:train,qaps:qaps.csv" 
            --from_format="narrativeqa" 
            --to_format="squad" 
            --to_file_name="train.json" #it is gonna be renamed as "[from_to]_filename.what"
            """

            story_summary_content = UTIL.load_csv_file(source_file, ",", 'infer', logging)
            question_content = UTIL.load_csv_file(source_files['qaps'], ",", 'infer', logging)
            set_type = source_files['set']
            formatted_content = narrativeqa.convert_to_squad(story_summary_content, question_content, set_type)
            UTIL.dump_json_file(destination_file, formatted_content, logging)

        elif args.from_format.lower() == 'webqa' and args.to_format.lower() == 'squad':
            " ************************************************************ "
            " *********************** ON-HOLD *****************************"
            " ************************************************************ "
            """            
            --log_path="~/log.log" 
            --data_path="~/data/" 
            --from_files="label:question.train.token_idx.label,voc:vocabulary,answer:answers.label.token_idx" 
            --from_format="webqa" 
            --to_format="squad"
            --to_file_name="filename.what" #it is gonna be renamed as "[from_to]_filename.what" 
            """

            story_summary_content = UTIL.load_csv_file(source_file, ",", 'infer', logging)
            question_content = UTIL.load_csv_file(source_files['qaps'], ",", 'infer', logging)
            set_type = source_files['set']
            formatted_content = narrativeqa.convert_to_squad(story_summary_content, question_content, set_type)
            UTIL.dump_json_file(args.destination_file_path, formatted_content, logging)
        elif args.from_format.lower() == 'msmarco' and args.to_format.lower() == 'squad':
            """            
            --log_path="~/log.log" 
            --data_path="~/data/msmarco"
            --from_format="msmarco" 
            --to_format="squad"
            --to_file_name="dev_2.1.json" #it is gonna be renamed as "[from_to]_filename.what" 
            """
            input_dict = {}
            try:
                version = float(source_files['v'])
            except:
                version = 2.0

            input_dict['v'] = version
            if version <= 2.0:
                """
                for version <= 2.0
                --from_files="source:dev_2.1.json, v:2.0"
                """
                in_content = UTIL.load_json_file(source_file, logging)
                input_dict['story_question_content'] = in_content
                formatted_content = msmarco.convert_to_squad(in_content)
            else:
                """
                for version > 2.0
                --from_files="source:queries.train.csv,document:collection.tsv,mapping:qrels.train.csv,v:2.1,limit:-1"
                """
                queries = UTIL.load_csv_file(source_file, "\t", None, logging, ['id', 'content'])
                input_dict['queries'] = queries
                mappings = UTIL.load_csv_file(source_files['mapping'], "\t", None, logging, ['q_id', 'tmp1', 'p_id', 'tmp2'], [0,1,2,3])
                input_dict['mappings'] = mappings
                documents = UTIL.load_csv_file(source_files['document'], "\t", None, logging, ['id', 'content'])
                input_dict['documents'] = documents
                input_dict['limit'] = int(source_files['limit'])
                formatted_content = msmarco.convert_to_squad(input_dict)
            UTIL.dump_json_file(destination_file, formatted_content, logging)
        elif args.from_format.lower() == 'quasar' and args.to_format.lower() == 'squad':
            """            
            --log_path="~/log.log" 
            --data_path="~/data/quasar-t"
            --from_format="quasar-t" 
            --to_format="squad"
            --from_files="source:train_questions.json,document:train_contexts.json,type:t,is_null_tags_filter, limit:-1"
            --to_file_name="train.json"
            """
            if source_files['type'].lower() =='t':
                # quasar-t
                queries = UTIL.load_json_line_file(source_file, logging)
                documents = UTIL.load_json_line_file(source_files['document'], logging)
                formatted_content = quasar.convert_to_squad(queries, documents, source_files['is_null_tags_filter'], int(source_files['limit']))
            UTIL.dump_json_file(destination_file, formatted_content, logging)

        elif args.from_format.lower() == 'ubuntu' and args.to_format.lower() == 'squad':
            """            
            --log_path="~/log.log" 
            --data_path="~/data/ubuntu" 
            --from_files="source:valid.csv"
            --from_format="ubuntu" 
            --to_format="squad"
            --to_file_name="valid.json"
            """
            story_question_content = UTIL.load_csv_file(source_file, ",", 'infer', logging)
            formatted_content = ubuntudialogue.convert_to_squad(story_question_content)
            UTIL.dump_json_file(destination_file, formatted_content, logging)
        elif args.from_format.lower() == 'newsqa' and args.to_format.lower() == 'squad':

            """            
            --log_path="~/log.log" 
            --data_path="~/data/newsqa" 
            --from_files="source:newsqa-data-v1.csv,story:cnn_stories/"
            --from_format="newsqa" 
            --to_format="squad"
            --to_file_name="news.json"
            """

            story_question_content = UTIL.load_csv_file(source_file, ",", 'infer', logging)
            context_content_path = source_files['story']
            formatted_content = cnnnews.convert_to_squad(story_question_content, context_content_path)
            UTIL.dump_json_file(destination_file, formatted_content, logging)
        else:
            pass
        logging.info('(function {}) Finished'.format(main.__name__))
    except Exception as e:
        logging.error('(function {}) has an error: {}'.format(main.__name__, e))
        raise
if __name__ == '__main__':
    args = get_parser().parse_args()
    assert args.log_path is not None, "No log path found at {}".format(args.log_path)
    assert args.data_path is not None, "No folder path found at {}".format(args.data_path)
    assert args.from_format is not None, "No 'from format' found {}".format(args.from_format)
    assert args.from_files is not None, "No 'from files' format found {}".format(args.from_files)
    assert args.to_format is not None, "No 'to format' dataset format found {}".format(
        args.to_format)
    assert args.to_file_name is not None, "No 'to file name' dataset format found {}".format(
        args.to_file_name)

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