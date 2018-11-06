def convert_to_squad(story_question_content):
    """
    :param story_question_content::
    :return: formatted SQUAD data
    At initial version, we are just focusing on the context and question, nothing more,
    therefore we are ignoring the answer part as of now
    """
    squad_formatted_content = dict()
    squad_formatted_content['version'] = 'wikiqa_squad_format'
    data = []
    grouped = story_question_content.groupby(['QuestionID'])
    for q, datum in grouped:

        datum = datum.loc[datum['Label'].isin([1])]
        #anyRelatedLabel = sum(datum['Label'])
        if len(datum) > 0:

            # Format is deeply nested JSON -- prepare data structures
            data_ELEMENT = dict()
            data_ELEMENT['title'] = datum.iloc[0]['DocumentTitle']
            paragraphs = []
            paragraphs_ELEMENT = dict()
            qas = []
            qas_ELEMENT = dict()
            qas_ELEMENT_ANSWERS = []
            ANSWERS_ELEMENT = dict()

            qas_ELEMENT['id'] = q
            qas_ELEMENT['question'] = datum.iloc[0]['Question']

            superdocument = ' '.join(datum['Sentence'].tolist())

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