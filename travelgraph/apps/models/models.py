import pdb
import json
import hashlib
import random
from datetime import datetime

from travelgraph import settings
from travelgraph.apps.database import postgre, cursor

from travelgraph.apps.models import (
        models_questions,
        models_tags,
        models_answers
    )


'''
Types of methods - 
1.normal
2.facebook
3.google
4.twitter
'''


def get_random_word(wordLen):
    word = ''
    for i in range(wordLen):
        word += random.choice(('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrs'
                               'tuvwxyz0123456789/&='))
    return word


def get_unique_username(first_name, last_name):
    '''
    This is to generate a unique username
    '''

    username = '{0}-{1}-1'.format(first_name.lower(), last_name.lower())

    query = """ SELECT * FROM "user"
                WHERE username = '{0}' """.format(username)

    cursor.execute(query)

    total_results = len(cursor.fetchall())

    username = username.split('-')
    username[2] = str(total_results+1)
    username = '-'.join(username)

    return username


def create_user(email, method=None, **kwargs):
    '''
    This function adds user to the database
    '''

    first_name = kwargs.get('first_name')
    last_name  = kwargs.get('last_name')
    profile_photo = kwargs.get('profile_photo','')

    created_ts = datetime.now()
    updated_ts = datetime.now()

    # Add a function which sees how many users of the same name are there
    # Then add the no.
    
    username = get_unique_username(first_name, last_name)

    # MD5 Hashing, because ethics
    password = hashlib.md5(kwargs.get('password')).hexdigest()

    bio = kwargs.get('bio')

    query = """ SELECT * FROM "user"
        WHERE email = '{0}' """.format(email)

    cursor.execute(query)
    result = cursor.fetchall()
    
    response = {}

    if method == 'normal':
        '''
        Normal Signup
        '''

        # If a user with the same email already exists, an error response is returned
        if len(result) != 0:
            response.update({
                'status':'failed',
                'error':'A user with the same email already exists',
            })

            return json.dumps(response)

        query = """ INSERT INTO "user" 
            (email, username, password, updated_ts,
                created_ts, first_name, last_name, bio, profile_photo)
            VALUES ('{0}', '{1}', '{2}', '{3}',
                '{4}', '{5}', '{6}', '{7}', '{8}')""".format(
                email, username, password, updated_ts,
                created_ts, first_name, last_name, bio, profile_photo)

        cursor.execute(query)
        postgre.commit()

        auth_user(email, method='facebook')

        response.update({
            'status':'success',
            'message':'user signed up normally',
            'name':first_name + last_name,
        })

        return response

    elif method == 'facebook':
        
        password = hashlib.md5(get_random_word(10)).hexdigest()
        
        # To see if user has already signed up and wants to login
        if len(result) != 0:
            #pdb.set_trace()
            response = auth_user(result[0]['email'], method, **kwargs)
            return response


        else:
            query = """ INSERT INTO "user" 
            (email, username, password, updated_ts,
                created_ts, first_name, last_name, profile_photo)
            VALUES ('{0}', '{1}', '{2}', '{3}',
                '{4}', '{5}', '{6}', '{7}')""".format(
                email, username, password, updated_ts,
                created_ts, first_name, last_name, profile_photo)

            cursor.execute(query)
            postgre.commit()

            return json.dumps({'status': 'success','message': 'user add fb'})

    return 'Done, also add exception here'


def auth_user(email, method=None, **kwargs):
    '''
    Sees whether user-info is correct
    '''

    response = {}

    if method == 'normal':
        '''
        Normal Login Method
        '''

        password = hashlib.md5(kwargs.get('password')).hexdigest()

        query = """ SELECT * FROM "user"
            WHERE email = '{0}' AND
            password = '{1}' """.format(email, password)

        cursor.execute(query)
        result = cursor.fetchone()

        # Email Password combination does not match
        if not result:
            response.update({
                'status': 'failed',
                'error':' Email Password combination does not match'
            })

            return response

        else:
            # Start session here
            response.update({
                'status': 'success',
                'message': 'user-info is correct',
                'user_id': result['user_id'],
                'username': result['username']
            })
            return response

    elif method == 'facebook':
        '''
        Login through Facebook
        ''' 
        
        query = """ SELECT * FROM "user"
            WHERE email = '{0}' """.format(email)

        cursor.execute(query)
        result = cursor.fetchall()

        # This means the user is not signed up, so lets send him to signup
        if len(result) == 0:
            response = create_user(email, method, **kwargs)
            return response
        else:
            response = {
                'status': 'success',
                'message': 'user-info is correct',
                'user_id': result[0]['user_id'],
                'username': result[0]['username'],
            }
            return response


def user_follows_user(user_id, user_id_to_follow):
    '''
    When a user follows another user
    '''

    response = {}

    created_ts = datetime.now()

    query = """ INSERT INTO "user_follows"
                (user_id, follows_user_id,created_ts) 
                VALUES ('{0}', '{1}', '{2}') """.format(user_id,
                                user_id_to_follow, created_ts)

    cursor.execute(query)
    postgre.commit()

    response.update({
        'status':'success',
        'message':'User {0} is now following User {1}'.format(user_id,
                                                        user_id_to_follow)
    })

    return response


def get_followers(user_id):
    '''
    Get a list of all the user_ids that follow the given user_id
    '''

    response = []

    query = """ SELECT * FROM "user_follows"
                WHERE follows_user_id = '{0}' """.format(user_id)

    cursor.execute(query)
    result = cursor.fetchall()

    for row in result:
        response.append(row['user_id'])

    return response


def get_following(user_id):
    '''
    Get a list of all the user_ids that are followed by the given user_id
    '''

    response = []

    query = """ SELECT * FROM "user_follows"
                WHERE user_id = '{0}' """.format(user_id)

    cursor.execute(query)
    result = cursor.fetchall()

    for row in result:
        response.append(row['follows_user_id'])

    return response


def user_profile(user_id):
    '''
    Load user specific details for his/her profile
    '''

    response = {
        'user_id': user_id,
    }

    query_user_data = """ SELECT * FROM "user"
                          WHERE user_id = '{0}' """.format(user_id)

    cursor.execute(query_user_data)
    user_data = cursor.fetchone()
    # Above user_data should be looked into and should be converted into a proper dictionary
    user_data = user_details(user_id)

    user_questions = models_questions.get_user_questions(user_id)['questions']

    user_answers = models_answers.get_user_answer(user_id)['answers']

    user_answered_question_ids = [ question['question_id'] 
                                   for question 
                                   in user_answers ]

    user_answered_questions = [ models_questions.get_question(question)
                                for question
                                in user_answered_question_ids ]

    user_following = get_following(user_id)

    user_followers = get_followers(user_id)

    user_tags = models_tags.get_user_tags(user_id)['tags']

    response.update({
        'status': 'success',
        'user_data': user_data,
        'user_questions': user_questions,
        'user_answers': user_answers,
        'user_answered_questions': user_answered_questions,
        'user_following': user_following,
        'user_followers': user_followers,
        'user_tags': user_tags,
    })

    return response


def user_details(user_id):
    '''
    Get some details about the asker of a question
    '''

    user_details = {}

    query = """ SELECT * FROM "user"
                WHERE user_id = '{0}' """.format(user_id)

    cursor.execute(query)
    user_data = cursor.fetchone()

    user_details.update({
        'status': 'success',
        'user_id': user_data['user_id'],
        'first_name': user_data['first_name'],
        'last_name': user_data['last_name'],
        'email': user_data['email'],
        'username': user_data['username'],
        'profile_photo': user_data['profile_photo'],
    })

    return user_details

