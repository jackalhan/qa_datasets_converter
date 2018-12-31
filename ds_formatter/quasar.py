import pandas as pd
import numpy as np
from tqdm import tqdm
from sklearn.utils import shuffle

def convert_to_squad(queries, documents, is_null_tags_filter, limit):
    squad_formatted_content = dict()
    squad_formatted_content['version'] = 'quasar-t_squad_format'
    data=[]
    pairs = create_pairs(zip(queries, documents), is_null_tags_filter)
    # if limit != -1:
    #     pairs = shuffle(pairs)

    pairs = pairs.groupby(['p_id', 'p_content'])
    iterator =  tqdm(enumerate(pairs))
    for i, pack in iterator:
        if limit != -1 and i > limit:
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

def create_pairs(query_document_pair, is_null_tags_filter):
    pairs = []
    generator = enumerate(query_document_pair)
    for i, pair in generator:
        query, context = pair[0], pair[1]
        if is_null_tags_filter.lower() in ['true', 'True', 'TRUE']:
            if len(query['tags']) == 0:
                continue
        if query['uid'] != context['uid']:
            print(20 * '!')
            print('Query {} - Document {} is mismatched.'.format(query['uid'],context['uid']))
        pairs.append((query['uid'], query['question'], i, context['contexts'][0][1]))
    return pd.DataFrame(pairs, columns=['q_id', 'q_content', 'p_id', 'p_content'])
