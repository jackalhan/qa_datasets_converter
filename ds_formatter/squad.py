from tqdm import tqdm
import util as UTIL
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
#from random import shuffle,random
import os
import random
def convert_idx(text, tokens):
    current = 0
    spans = []
    for token in tokens:
        current = text.find(token, current)
        if current < 0:
            print("Token {} cannot be found".format(token))
            raise Exception()
        spans.append((current, current + len(token)))
        current += len(token)
    return spans

def process_squad_file(data, word_counter, char_counter):
    print("Generating examples...")
    examples = []
    eval_examples = {}
    total,_i_para  = 0, 0
    questions = []
    paragraphs = []
    question_to_paragraph = []
    for article in tqdm(data["data"]):
        title = article["title"]
        for para in article["paragraphs"]:
            context = para["context"].replace(
                "''", '" ').replace("``", '" ')
            paragraphs.append(context)
            context_tokens = UTIL.word_tokenize(context)
            context_chars = [list(token) for token in context_tokens]
            spans = convert_idx(context, context_tokens)
            for token in context_tokens:
                word_counter[token] += len(para["qas"])
                for char in token:
                    char_counter[char] += len(para["qas"])
            for qa in para["qas"]:
                total += 1
                ques = qa["question"].replace(
                    "''", '" ').replace("``", '" ')
                questions.append(ques)
                question_to_paragraph.append(_i_para)
                ques_tokens = UTIL.word_tokenize(ques)
                ques_chars = [list(token) for token in ques_tokens]
                for token in ques_tokens:
                    word_counter[token] += 1
                    for char in token:
                        char_counter[char] += 1
                y1s, y2s = [], []
                answer_texts = []
                for answer in qa["answers"]:
                    answer_text = answer["text"]
                    answer_start = answer['answer_start']
                    answer_end = answer_start + len(answer_text)
                    answer_texts.append(answer_text)
                    answer_span = []
                    for idx, span in enumerate(spans):
                        if not (answer_end <= span[0] or answer_start >= span[1]):
                            answer_span.append(idx)
                    y1, y2 = answer_span[0], answer_span[-1]
                    y1s.append(y1)
                    y2s.append(y2)
                example = {"context_tokens": context_tokens, "context_chars": context_chars, "ques_tokens": ques_tokens,
                           "ques_chars": ques_chars, "y1s": y1s, "y2s": y2s, "id": total}
                examples.append(example)
                eval_examples[str(total)] = {
                    "context": context, "spans": spans, 'ques': ques,"answers": answer_texts, "uuid": qa["id"], 'title': title}
            _i_para += 1
    print("{} questions in total".format(len(examples)))
    return examples, eval_examples, questions, paragraphs, question_to_paragraph
def tokenize_contexts(contexts:list, max_tokens=-1):
    tokenized_context = [UTIL.word_tokenize(context.strip()) if max_tokens == -1 else UTIL.word_tokenize(context.strip())[0:max_tokens]for context in contexts]
    return tokenized_context

def fixing_the_token_problem(tokenized_questions, tokenized_paragraphs):
    # fixing the '' problem:
    fixed_tokenized_question = []
    for indx, question in enumerate(tokenized_questions):
        tokens = []
        for token in question:
            t = token.strip()
            if t != "":
                tokens.append(t)
        fixed_tokenized_question.append(tokens)

    fixed_tokenized_paragraph = []
    for indx, paragraph in enumerate(tokenized_paragraphs):
        tokens = []
        for token in paragraph:
            t = token.strip()
            if t != "":
                tokens.append(t)
        fixed_tokenized_paragraph.append(tokens)
    return fixed_tokenized_question, fixed_tokenized_paragraph

def yield_to_matchzoo(question_answer_content, q_len, negative_sampling_count=100, max_tokens=-1):
    """
    :param question_answer_document content:
    :return: yield matchzoo data
    At initial version, we are just focusing on the context and question, nothing more,
    therefore we are ignoring the answer part as of now
    """
    word_counter, char_counter = Counter(), Counter()
    examples, eval, questions, paragraphs, q_to_ps = process_squad_file(question_answer_content, word_counter, char_counter)
    tokenized_paragraphs = tokenize_contexts(paragraphs, max_tokens)
    tokenized_questions = tokenize_contexts(questions, max_tokens)
    tokenized_questions, tokenized_paragraphs = fixing_the_token_problem(tokenized_questions, tokenized_paragraphs)

    paragraphs_nontokenized = [" ".join(context) for context in tokenized_paragraphs]
    questions_nontokenized = [" ".join(context) for context in tokenized_questions]

    for q_indx, question in enumerate(tqdm(questions_nontokenized[0:q_len])):
        true_p_indx = q_to_ps[q_indx]
        true_paragraph = paragraphs_nontokenized[true_p_indx]
        temp_list = paragraphs_nontokenized.copy()
        del temp_list[true_p_indx]
        random.Random(q_indx).shuffle(temp_list)
        for p_indx, paragraph in enumerate([true_paragraph] + temp_list[:negative_sampling_count-1]):
            yield '\t'.join(['1' if p_indx == 0 else '0', question, paragraph])
def convert_to_lucene(question_answer_content, doc_type_verbose, source_path):
    """
    :param question_answer_document content:
    :return: yield matchzoo data
    At initial version, we are just focusing on the context and question, nothing more,
    therefore we are ignoring the answer part as of now
    """
    word_counter, char_counter = Counter(), Counter()
    examples, eval, questions, paragraphs, q_to_ps = process_squad_file(question_answer_content, word_counter, char_counter)
    tokenized_paragraphs = tokenize_contexts(paragraphs, -1)
    tokenized_questions = tokenize_contexts(questions, -1)
    tokenized_questions, tokenized_paragraphs = fixing_the_token_problem(tokenized_questions, tokenized_paragraphs)

    paragraphs_nontokenized = [" ".join(context) for context in tokenized_paragraphs]
    questions_nontokenized = [" ".join(context) for context in tokenized_questions]

    if doc_type_verbose == 1 or doc_type_verbose == 3:
        # questions
        print('Questions are getting dumped.')
        dst_dir = UTIL.create_dir(os.path.join(source_path, 'lucene_questions'))
        for indx, doc in tqdm(enumerate(questions_nontokenized)):
            as_json = dict()
            as_json['content'] = doc
            #as_json['doc_id'] = indx
            UTIL.dump_json_file(os.path.join(dst_dir, '{}.json'.format(indx)), as_json, None)
    elif doc_type_verbose == 2 or doc_type_verbose == 3:
        print('Paragraphs are getting dumped.')
        dst_dir = UTIL.create_dir(os.path.join(source_path, 'lucene_paragraphs'))
        for indx, doc in tqdm(enumerate(paragraphs_nontokenized)):
            as_json = dict()
            as_json['content'] = doc
            #as_json['doc_id'] = indx
            UTIL.dump_json_file(os.path.join(dst_dir, '{}.json'.format(indx)), as_json, None)
    print('Completed.')

def print_statistics(question_answer_content, is_histogram, histogram_bin,  document_type):
    word_counter, char_counter = Counter(), Counter()
    examples, eval, questions, paragraphs, q_to_ps = process_squad_file(question_answer_content, word_counter,
                                                                        char_counter)
    tokenized_paragraphs = tokenize_contexts(paragraphs, -1)
    tokenized_questions = tokenize_contexts(questions, -1)
    tokenized_questions, tokenized_paragraphs = fixing_the_token_problem(tokenized_questions, tokenized_paragraphs)

    paragraphs_nontokenized = [" ".join(context) for context in tokenized_paragraphs]
    questions_nontokenized = [" ".join(context) for context in tokenized_questions]

    data = []
    corpus = []
    if document_type in [1, 3]:
        corpus = corpus + tokenized_questions
    if document_type in [2, 3]:
        corpus = corpus + tokenized_paragraphs
    for doc in corpus:
        data.append(len(doc))

    if is_histogram.lower() in ['true', 'True', 'TRUE']:
        data_df = pd.DataFrame(data, columns=['doc_len'])
        data_df.hist(bins=histogram_bin)
        plt.show()



def convert_to_short_squad(question_answer_content, q_len, negative_sampling_count, max_tokens=-1):
    word_counter, char_counter = Counter(), Counter()
    examples, eval, questions, paragraphs, q_to_ps = process_squad_file(question_answer_content, word_counter,
                                                                        char_counter)
    tokenized_paragraphs = tokenize_contexts(paragraphs, max_tokens)
    tokenized_questions = tokenize_contexts(questions, max_tokens)
    tokenized_questions, tokenized_paragraphs = fixing_the_token_problem(tokenized_questions, tokenized_paragraphs)

    paragraphs_nontokenized = [" ".join(context) for context in tokenized_paragraphs]
    questions_nontokenized = [" ".join(context) for context in tokenized_questions]

    squad_formatted_content = dict()
    squad_formatted_content['version'] = 'short_squad_format'
    data = []

    last_paragraph_indx = None
    questions = []

    for q_indx, question in enumerate(tqdm(questions_nontokenized[0:q_len])):
        if len(data) > negative_sampling_count:
            break
        if last_paragraph_indx is None:
            last_paragraph_indx = q_to_ps[q_indx]
        #qs = [i for i in q_to_ps if i == 0]
        current_paragraph_indx = q_to_ps[q_indx]

        if current_paragraph_indx != last_paragraph_indx:
            data_ELEMENT = dict()
            data_ELEMENT['title'] = 'dummyTitle'
            paragraphs = []
            paragraphs_ELEMENT = dict()
            superdocument = paragraphs_nontokenized[last_paragraph_indx]
            paragraphs_ELEMENT['context'] = superdocument
            qas = []
            for _q_item in questions:
                _q_indx, _q = _q_item[0], _q_item[1]
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
            questions = []
            last_paragraph_indx = current_paragraph_indx
        questions.append((q_indx, question))
    squad_formatted_content['data'] = data
    return squad_formatted_content