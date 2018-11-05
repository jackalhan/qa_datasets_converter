def convert_to_squad(questions, answers, a_to_q_map):
    """
    questions:questions
    answers: answers or context or paragraphs
    a_to_q_map: answers to questions mapping
    """
    squad_formatted_content = dict()
    squad_formatted_content['version'] = 'insuranceqa_squad_format'
    data = []


    for par_indx, ques in a_to_q_map.items():
        # Format is deeply nested JSON -- prepare data structures
        data_ELEMENT = dict()
        data_ELEMENT['title'] = 'dummyTitle'

        paragraphs = []
        paragraphs_ELEMENT = dict()

        superdocument = answers[par_indx]
        paragraphs_ELEMENT['context'] = superdocument


        qas = []
        for q_indx in ques:
            qas_ELEMENT = dict()
            ANSWERS_ELEMENT = dict()
            qas_ELEMENT_ANSWERS = []
            qas_ELEMENT['id'] = q_indx
            qas_ELEMENT['question'] = questions[q_indx]
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

def load_vocab(vocab_file):
  voc = {}
  with open(vocab_file, 'r') as f_in:
      for line in f_in:
        word, _id = line.strip().split('\t')
        voc[word] = _id
  return voc

def load_answers(answers_file, voc):
  #answers = context
  _list = ["None"]
  with open(answers_file, 'r') as f_in:
      for line in f_in:
          _, sent = line.strip().split('\t')
          _list.append(' '.join([voc[wid] for wid in sent.split(' ')]))
  return _list


def load_questions(question_file, voc):
  questions = []
  a_to_q_map = dict()
  x = dict()
  ground_truth, no_ground_truth = 0, 0
  with open(question_file, 'r') as f_in:
      for q_indx, line in enumerate(f_in):
        try:
            type, q = line.strip().split('\t')
        except:
            type, q, ids, pooled_answers = line.strip().split('\t')
        q = ' '.join([voc[wid] for wid in q.split(' ')])
        questions.append(q)
        if type not in x:
            x[type] = 1
        else:
            x[type] = x[type] + 1

        if len([1 for gt in ids.split(' ') if gt in pooled_answers.split(' ')]) <= 0:
            no_ground_truth +=1
        else:
            ground_truth += 1
            for _id in ids.split(' '):
                if _id not in a_to_q_map:
                    a_to_q_map[int(_id)] = [q_indx]
                else:
                    temp_qs = a_to_q_map[int(_id)]
                    temp_qs = temp_qs.append(int(_id))
                    a_to_q_map[int(_id)] = temp_qs
      print(x)
      print("Total items: {}".format(sum([v for k, v in x.items()])))
      print('Ground Truth: {}, No Ground_Truth: {}'.format(ground_truth, no_ground_truth))
  return questions, a_to_q_map