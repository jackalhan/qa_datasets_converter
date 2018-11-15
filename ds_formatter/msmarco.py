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

def convert_to_squad(story_question_content):
    """
    :param story_question_content:
    :return: formatted SQUAD data
    At initial version, we are just focusing on the context and question, nothing more,
    therefore we are ignoring the answer part as of now.
    The code is to process train and development sets of MS-MARCO, since test(eval) set doesn't has answer information
    """
    # PARSE FILES

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