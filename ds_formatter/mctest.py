def convert_to_squad(story_question_content):
    """
    :param story_question_content:
    :param answer_content:
    :return: formatted SQUAD data
    At initial version, we are just focusing on the context and question, nothing more,
    therefore we are ignoring the answer part as of now
    """
    # PARSE FILES

    squad_formatted_content = dict()
    squad_formatted_content['version'] = 'mctest_squad_format'
    data = []
    #TODO: Each context has multiple questions and each row of the file has multiple questions in different columns (like every 4 columns), we need to handle this.
    for datum in story_question_content.itertuples(index=False):
        # Format is deeply nested JSON -- prepare data structures
        data_ELEMENT = dict()
        data_ELEMENT['title'] = 'dummyTitle'

        paragraphs = []
        paragraphs_ELEMENT = dict()

        superdocument = datum[2].replace('\\newline', '')
        paragraphs_ELEMENT['context'] = superdocument

        qas = []
        # it has 4 questions in each context
        question_column_start_indx = 3
        question_size = 4
        for q_indx in range(question_size):
            qas_ELEMENT = dict()
            ANSWERS_ELEMENT = dict()
            qas_ELEMENT_ANSWERS = []
            qas_ELEMENT['id'] = datum[0] + "." +str(q_indx)
            qas_ELEMENT['question'] = datum[q_indx + question_column_start_indx if q_indx < 1 else q_indx * 5 + 3].replace("one: ", "").replace("multiple: ", "")
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