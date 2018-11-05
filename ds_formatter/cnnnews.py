def convert_to_squad(question_answer_content, context_content_path):
    """
    :param question_answer_content:
    :param context_content_path: story files folder path
    :return: formatted SQUAD data
    At initial version, we are just focusing on the context and question, nothing more,
    therefore we are ignoring the answer part as of now
    """
    # PARSE FILES
    import os

    squad_formatted_content = dict()
    squad_formatted_content['version'] = 'cnnnews_squad_format'
    data = []
    #TODO: Each context has multiple questions and each row of the file has multiple questions in different columns (like every 4 columns), we need to handle this.
    for datum in question_answer_content.itertuples(index=False):
        # Format is deeply nested JSON -- prepare data structures
        if datum[3] > 0 : #(part) answer absent, skip this question
            continue

        data_ELEMENT = dict()
        data_ELEMENT['title'] = 'dummyTitle'
        paragraphs = []
        paragraphs_ELEMENT = dict()
        qas = []
        qas_ELEMENT = dict()
        qas_ELEMENT_ANSWERS = []
        ANSWERS_ELEMENT = dict()

        story_file_name = datum[0][(datum[0].rindex('/') + 1):]
        qas_ELEMENT['id'] = story_file_name
        qas_ELEMENT['question'] = datum[1]

        story_file_path = context_content_path + os.sep + story_file_name
        if not os.path.isfile(story_file_path):
            raise TypeError(story_file_path + " does not exist")
        superdocument = open(story_file_path).read()

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