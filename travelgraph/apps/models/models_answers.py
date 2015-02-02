import pdb
import json

from travelgraph.apps.database import postgre, cursor


def add_answer(question_id, answer_text, user_id):
    '''
    Storing answer for a given question
    '''

    response = {}

    query = """ INSERT INTO "answers" (answer, question_id, user_id) 
                VALUES ('{0}', '{1}', '{2}') """.format(answer_text,
                                                question_id, user_id)

    cursor.execute(query)
    postgre.commit()

    response.update({
        'status': 'success',
        'message': 'Answer added successfully'
    })

    return response


def get_answer(answer_id):
    '''
    Retrieving the details of a single answer
    '''

    response = {}

    query = """ SELECT * FROM "answers"
                WHERE answer_id = '{0}' """.format(answer_id)

    cursor.execute(query)
    result = cursor.fetchone()

    if result:
        response.update({
            'answer_id': result['answer_id'],
            'answer': result['answer'],
            'question_id': result['question_id'],
            'user_id': result['user_id']
        })

    return response

def get_all_answers(question_id):
    '''
    Retrieving all the answers for a specific question
    '''

    response = {}

    response['answers'] = []

    response = {
        'answers': [],
    }

    answer_ids = []

    query = """ SELECT answer_id FROM "answers" 
                WHERE question_id = '{0}' """.format(question_id)

    result = cursor.fetchall()

    if result:
        for row in result:
            response['answers'].append(get_answer(row['answer_id']))

    response.update({
        'status': 'success',
        'message': '{0} answer(s) found'.format(len(response['answers'])),
        'question_id' : '{0}'.format(question_id)
    })

    return response