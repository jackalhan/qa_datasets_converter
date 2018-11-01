import random
from tqdm import tqdm
import nltk
sent_tokenize = nltk.data.load("tokenizers/punkt/english.pickle")
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import util as UTIL

def convert_to_squad_format(qa_content, wikipedia_dir, web_dir, sample_size, seed, max_num_of_tokens):
    qa_json = read_triviaqa_data(qa_content)
    qad_triples = get_qad_triples(qa_json)

    random.seed(seed)
    random.shuffle(qad_triples)

    data = []
    for qad in tqdm(qad_triples):
        qid = qad['QuestionId']

        text = get_text(qad, qad['Source'], web_dir, wikipedia_dir)
        selected_text = select_relevant_portion(text, max_num_of_tokens)

        question = qad['Question']
        para = {'context': selected_text, 'qas': [{'question': question, 'answers': []}]}
        data.append({'paragraphs': [para]})
        qa = para['qas'][0]
        qa['id'] = get_question_doc_string(qid, qad['Filename'])
        qa['qid'] = qid

        ans_string, index = answer_index_in_document(qad['Answer'], selected_text)
        if index == -1:
            if qa_json['Split'] == 'train':
                continue
        else:
            qa['answers'].append({'text': ans_string, 'answer_start': index})

        if qa_json['Split'] == 'train' and len(data) >= sample_size and qa_json['Domain'] == 'Web':
            break

    squad = {'data': data, 'version': qa_json['Version']}
    return squad


def read_triviaqa_data(trivia_content):
    data = trivia_content #UTIL.load_json_file(file_path=qajson, logging=None)
    # read only documents and questions that are a part of clean data set
    if data['VerifiedEval']:
        clean_data = []
        for datum in data['Data']:
            if datum['QuestionPartOfVerifiedEval']:
                if data['Domain'] == 'Web':
                    datum = read_clean_part(datum)
                clean_data.append(datum)
        data['Data'] = clean_data
    return data

def read_clean_part(datum):
    for key in ['EntityPages', 'SearchResults']:
        new_page_list = []
        for page in datum.get(key, []):
            if page['DocPartOfVerifiedEval']:
                new_page_list.append(page)
        datum[key] = new_page_list
    assert len(datum['EntityPages']) + len(datum['SearchResults']) > 0
    return datum

# Key for wikipedia eval is question-id. Key for web eval is the (question_id, filename) tuple
def get_key_to_ground_truth(data):
    if data['Domain'] == 'Wikipedia':
        return {datum['QuestionId']: datum['Answer'] for datum in data['Data']}
    else:
        return get_qd_to_answer(data)


def get_question_doc_string(qid, doc_name):
    return '{}--{}'.format(qid, doc_name)

def get_qd_to_answer(data):
    key_to_answer = {}
    for datum in data['Data']:
        for page in datum.get('EntityPages', []) + datum.get('SearchResults', []):
            qd_tuple = get_question_doc_string(datum['QuestionId'], page['Filename'])
            key_to_answer[qd_tuple] = datum['Answer']
    return key_to_answer

def answer_index_in_document(answer, document):
    answer_list = answer['NormalizedAliases']
    for answer_string_in_doc in answer_list:
        index = document.lower().find(answer_string_in_doc)
        if index != -1:
            return answer_string_in_doc, index
    return answer['NormalizedValue'], -1

def get_text(qad, domain, web_dir, wikipedia_dir):
    local_file = os.path.join(web_dir, qad['Filename']) if domain == 'SearchResults' else os.path.join(wikipedia_dir, qad['Filename'])
    return UTIL.get_file_contents(local_file, encoding='utf-8')


def select_relevant_portion(text, max_num_tokens):
    paras = text.split('\n')
    selected = []
    done = False
    for para in paras:
        sents = sent_tokenize.tokenize(para)
        for sent in sents:
            words = nltk.word_tokenize(sent)
            for word in words:
                selected.append(word)
                if len(selected) >= max_num_tokens:
                    done = True
                    break
            if done:
                break
        if done:
            break
        selected.append('\n')
    st = ' '.join(selected).strip()
    return st


def add_triple_data(datum, page, domain):
    qad = {'Source': domain}
    for key in ['QuestionId', 'Question', 'Answer']:
        qad[key] = datum[key]
    for key in page:
        qad[key] = page[key]
    return qad


def get_qad_triples(data):
    qad_triples = []
    for datum in data['Data']:
        for key in ['EntityPages', 'SearchResults']:
            for page in datum.get(key, []):
                qad = add_triple_data(datum, page, key)
                qad_triples.append(qad)
    return qad_triples