def convert_to_squad(story_question_content):
    """
    :param story_question_content:
    :return: formatted SQUAD data
    At initial version, we are just focusing on the context and question, nothing more,
    therefore we are ignoring the answer part as of now
    """
    # PARSE FILES

    squad_formatted_content = dict()
    squad_formatted_content['version'] = 'msmarco_squad_format'
    data = []
    query = story_question_content['query']
    query_keys = query.keys()
    passages = story_question_content['passages']

    id_index = 0
    for key in query_keys:
        # Format is deeply nested JSON -- prepare data structures
        data_ELEMENT = dict()
        data_ELEMENT['title'] = 'dummyTitle'
        paragraphs = []
        paragraphs_ELEMENT = dict()
        qas = []
        qas_ELEMENT = dict()
        qas_ELEMENT_ANSWERS = []
        ANSWERS_ELEMENT = dict()

        qas_ELEMENT['id'] = id_index
        qas_ELEMENT['question'] = query[key]
        id_index += 1

        superdocument = ' '.join([onePassage['passage_text'] for onePassage in passages[key]])

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