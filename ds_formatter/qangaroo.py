def convert_to_squad(source_data):
    """
    Converts QAngaroo data (hoppy_data) into SQuAD format.
    The SQuAD-formatted data is written to disk at write_file_name.
    Note: All given support documents per example are concatenated
        into one super-document. All text is lowercased.
    """
    squad_formatted_content = dict()
    squad_formatted_content['version'] = 'hoppy_squad_format'
    data = []


    for datum in source_data:

        # Format is deeply nested JSON -- prepare data structures
        data_ELEMENT = dict()
        data_ELEMENT['title'] = 'dummyTitle'
        paragraphs = []
        paragraphs_ELEMENT = dict()
        qas = []
        qas_ELEMENT = dict()
        qas_ELEMENT_ANSWERS = []
        ANSWERS_ELEMENT = dict()

        qas_ELEMENT['id'] = datum['id']
        qas_ELEMENT['question'] = datum['query']

        superdocument = " ".join(datum['supports'])

        answer_position = superdocument.find(datum['answer'])
        if answer_position == -1:
            continue

        ANSWERS_ELEMENT['answer_start'] = answer_position
        ANSWERS_ELEMENT['text'] = datum['answer']

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