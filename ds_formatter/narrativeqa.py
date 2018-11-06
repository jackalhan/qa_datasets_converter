def convert_to_squad(story_summary_content, question_content, set_type):
    """
    :param story_summary_content:
    :param question_content:
    :param category_content:
    :param set_type:
    :return: formatted SQUAD data
    At initial version, we are just focusing on the context and question, nothing more,
    therefore we are ignoring the answer part as of now
    """
    squad_formatted_content = dict()
    squad_formatted_content['version'] = 'narrativeqa_squad_format'
    data = []
    content = story_summary_content
    if set_type != 'all':
        content = story_summary_content[story_summary_content['set'] == set_type]

    for datum in content.itertuples(index=False):
        #print(datum.summary)
        data_ELEMENT = dict()
        data_ELEMENT['title'] = 'dummyTitle'

        paragraphs = []
        paragraphs_ELEMENT = dict()

        superdocument = datum.summary
        paragraphs_ELEMENT['context'] = superdocument

        qas = []
        sub_datum = question_content[question_content['document_id'] == datum.document_id]
        for q_datum in sub_datum.itertuples():
            # print(indx)
            #print(q_datum)
            qas_ELEMENT = dict()
            ANSWERS_ELEMENT = dict()
            qas_ELEMENT_ANSWERS = []
            qas_ELEMENT['id'] = q_datum.document_id + '-' + str(q_datum.Index)
            qas_ELEMENT['question'] = q_datum.question
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