import numpy as np
import pandas as pd
from tqdm import tqdm
from sklearn.utils import shuffle

# def convert_to_squad(story_question_content):
#     """
#     :param story_question_content:
#     :return: formatted SQUAD data
#     At initial version, we are just focusing on the context and question, nothing more,
#     therefore we are ignoring the answer part as of now
#     """
#     # PARSE FILES
#
#     squad_formatted_content = dict()
#     squad_formatted_content['version'] = 'msmarco_squad_format'
#     data = []
#     query = story_question_content['query']
#     query_keys = query.keys()
#     passages = story_question_content['passages']
#
#     id_index = 0
#     for key in query_keys:
#         # Format is deeply nested JSON -- prepare data structures
#         data_ELEMENT = dict()
#         data_ELEMENT['title'] = 'dummyTitle'
#         paragraphs = []
#         paragraphs_ELEMENT = dict()
#         qas = []
#         qas_ELEMENT = dict()
#         qas_ELEMENT_ANSWERS = []
#         ANSWERS_ELEMENT = dict()
#
#         qas_ELEMENT['id'] = id_index
#         qas_ELEMENT['question'] = query[key]
#         id_index += 1
#
#         superdocument = ' '.join([onePassage['passage_text'] for onePassage in passages[key]])
#
#         ANSWERS_ELEMENT['answer_start'] = -1
#         ANSWERS_ELEMENT['text'] = 'dummyAnswer'
#
#         paragraphs_ELEMENT['context'] = superdocument
#         qas_ELEMENT_ANSWERS.append(ANSWERS_ELEMENT)
#
#         qas_ELEMENT['answers'] = qas_ELEMENT_ANSWERS
#         qas.append(qas_ELEMENT)
#
#         paragraphs_ELEMENT['qas'] = qas
#         paragraphs.append(paragraphs_ELEMENT)
#
#         data_ELEMENT['paragraphs'] = paragraphs
#         data.append(data_ELEMENT)
#
#     squad_formatted_content['data'] = data
#
#     return squad_formatted_content
def convert_to_squad(input_dict):
    """
    :param story_question_content:
    :return: formatted SQUAD data
    At initial version, we are just focusing on the context and question, nothing more,
    therefore we are ignoring the answer part as of now.
    The code is to process train and development sets of MS-MARCO, since test(eval) set doesn't has answer information
    """
    # PARSE FILES
    squad_formatted_content=None
    if input_dict['v'] <= 2.0:
        squad_formatted_content = convert_v2(input_dict)
    else:
        squad_formatted_content = convert_v21(input_dict)
    return squad_formatted_content

def convert_v21(input_dict):
    squad_formatted_content = dict()
    squad_formatted_content['version'] = 'msmarco_v21_squad_format'
    data=[]
    all_data = assign_mapped_document(input_dict['queries'], input_dict['mappings'], input_dict['documents'])
    # if input_dict['limit'] != -1:
    #     all_data = shuffle(all_data)

    all_data = all_data.groupby(['p_id', 'p_content'])
    iterator = tqdm(enumerate(all_data))
    for i, pack in iterator:
        if input_dict['limit'] != -1 and i > input_dict['limit']:
            print('Data is prepared at the index of {}'.format(i))
            iterator.close()
            break
        p, qs = pack[0], pack[1]
        data_ELEMENT = dict()
        data_ELEMENT['title'] = 'dummyTitle'
        paragraphs = []
        paragraphs_ELEMENT = dict()
        superdocument = p[1]
        paragraphs_ELEMENT['context'] = superdocument
        qas = []
        for q in qs.itertuples():
            _q_indx, _q = q.q_id, q.q_content
            qas_ELEMENT = dict()
            ANSWERS_ELEMENT = dict()
            qas_ELEMENT_ANSWERS = []
            qas_ELEMENT['id'] = _q_indx
            qas_ELEMENT['question'] = _q
            ANSWERS_ELEMENT['answer_start'] = -1
            ANSWERS_ELEMENT['text'] = 'dummyAnswer'
            qas_ELEMENT_ANSWERS.append(ANSWERS_ELEMENT)
            qas_ELEMENT['answers'] = qas_ELEMENT_ANSWERS
            qas.append(qas_ELEMENT)
        paragraphs_ELEMENT['qas'] = qas
        paragraphs.append(paragraphs_ELEMENT)

        data_ELEMENT['paragraphs'] = paragraphs
        data.append(data_ELEMENT)
    squad_formatted_content['data'] = data
    return squad_formatted_content
def assign_mapped_document(queries, mappings, documents):
    # queries ids
    print('Shape of query is {}'.format(queries.shape))
    queries_mask = np.isin(mappings['q_id'], queries['id'])
    mappings = mappings[queries_mask]
    queries_dict = pd.Series(queries["content"].values, index=queries['id']).to_dict()
    print('Len of query dict is {}'.format(len(queries_dict)))
    print('Shape of mapping is {}'.format(mappings.shape))

    document_mask = np.isin(documents['id'], mappings['p_id'])
    documents = documents[document_mask]
    print('Shape of documents is {}'.format(documents.shape))

    documents_dict = pd.Series(documents["content"].values, index=documents['id']).to_dict()
    print('Len of document dict is {}'.format(len(documents_dict)))


    mappings['q_content'] = mappings['q_id'].map(queries_dict)
    mappings['p_content'] = mappings['p_id'].map(documents_dict)
    print('Shape of new mapping is {}'.format(mappings.shape))
    return mappings
def convert_v2(input_dict):
    """
    :param story_question_content:
    :return: formatted SQUAD data
    At initial version, we are just focusing on the context and question, nothing more,
    therefore we are ignoring the answer part as of now.
    The code is to process train and development sets of MS-MARCO, since test(eval) set doesn't has answer information
    """
    # PARSE FILES
    story_question_content = input_dict['story_question_content']
    squad_formatted_content = dict()
    squad_formatted_content['version'] = 'msmarco_squad_format'
    data = []
    query = story_question_content['query']
    #key list consists of keys of queries with answers
    keys_with_answer = [x for x, y in story_question_content['answers'].items() if y[0] != 'No Answer Present.' and y[0] != '']
    passages = story_question_content['passages']

    for key in keys_with_answer:
        # Format is deeply nested JSON -- prepare data structures
        data_ELEMENT = dict()
        data_ELEMENT['title'] = 'dummyTitle'
        paragraphs = []
        paragraphs_ELEMENT = dict()
        qas = []
        qas_ELEMENT = dict()
        qas_ELEMENT_ANSWERS = []
        ANSWERS_ELEMENT = dict()

        qas_ELEMENT['id'] = key
        qas_ELEMENT['question'] = query[key]

        #correct_context is a list
        correct_context= [x for x in passages[key] if x['is_selected'] == 1]
        #some query(question) has more than 1 correct contexts, we just pick the first one as the context
        if len(correct_context) == 0:
            continue
        superdocument = correct_context[0]['passage_text']

        ANSWERS_ELEMENT['answer_start'] = -1
        ANSWERS_ELEMENT['text'] = 'dummyAnswer'

        paragraphs_ELEMENT['context'] = superdocument
        qas_ELEMENT_ANSWERS.append(ANSWERS_ELEMENT)

        qas_ELEMENT['answers'] = qas_ELEMENT_ANSWERS
        qas.append(qas_ELEMENT)

        paragraphs_ELEMENT['qas'] = qas
        paragraphs.append(paragraphs_ELEMENT)

        data_ELEMENT['paragraphs'] = paragraphs
        data.append(data_ELEMENT)

    squad_formatted_content['data'] = data

    return squad_formatted_content