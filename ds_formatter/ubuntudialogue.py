def convert_to_squad(story_question_content):
    """
    :param story_question_content:
    :return: formatted SQUAD data
    At initial version, we are just focusing on the context and question, nothing more,
    therefore we are ignoring the answer part as of now
    """
    # PARSE FILES

    squad_formatted_content = dict()
    squad_formatted_content['version'] = 'ubuntudialogue_squad_format'
    data = []

    df = story_question_content.values
#    print(df.shape)
    id_index = 0
    # for valid and test dataset
    if(df.shape[1] == 11):
        for datum in df:
            data_ELEMENT = dict()
            data_ELEMENT['title'] = 'dummyTitle'
            paragraphs = []
            paragraphs_ELEMENT = dict()
            qas = []
            qas_ELEMENT = dict()
            qas_ELEMENT_ANSWERS = []
            ANSWERS_ELEMENT = dict()

            qas_ELEMENT['id'] = id_index
            id_index += 1
            qas_ELEMENT['question'] = datum[1].replace("__eou__ __eot__", ".").replace("__eou__", ".").replace("__eot__", ".")

            superdocument = datum[0].replace("__eou__ __eot__", ".").replace("__eou__", ".").replace("__eot__", ".")

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
    elif(df.shape[1] == 3): #for train set
        true_response = [x for x in df if x[2] == 1]
        for datum in true_response:
            data_ELEMENT = dict()
            data_ELEMENT['title'] = 'dummyTitle'
            paragraphs = []
            paragraphs_ELEMENT = dict()
            qas = []
            qas_ELEMENT = dict()
            qas_ELEMENT_ANSWERS = []
            ANSWERS_ELEMENT = dict()

            qas_ELEMENT['id'] = id_index
            id_index += 1
            qas_ELEMENT['question'] = datum[1].replace("__eou__ __eot__", ".").replace("__eou__", ".").replace("__eot__", ".")

            superdocument = datum[0].replace("__eou__ __eot__", ".").replace("__eou__", ".").replace("__eot__", ".")

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