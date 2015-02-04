import pdb
import json
import hashlib
import random
from datetime import datetime

from travelgraph import settings
from travelgraph.apps.database import postgre, cursor
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


def create_user(email, method=None, **kwargs):
    '''
    This function adds user to the database
    '''

    first_name = kwargs.get('first_name')
    last_name  = kwargs.get('last_name')

    created_ts = datetime.now()
    updated_ts = datetime.now()

    # Add a function which sees how many users of the same name are there
    # Then add the no.
    username = first_name.lower() + '-' +last_name.lower()

    # MD5 Hashing, because ethics
    password = hashlib.md5(kwargs.get('password')).hexdigest()

    # Generating the api key
    api_key = hashlib.sha256(get_random_word(15)).hexdigest()
    api_key = api_key[:15]

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
            (email, name, password, api_key,
                created_ts, first_name, last_name)
            VALUES ('{0}', '{1}', '{2}', '{3}',
                '{4}', '{5}', '{6}')""".format(
                email, username, password, api_key,
                created_ts, first_name, last_name)

        cursor.execute(query)
        postgre.commit()

        response.update({
            'status':'success',
            'message':'user signed up normally',
            'name':first_name + last_name,
        })

        return response

    elif method == 'facebook':
        
        # To see if user has already signed up and wants to login
        if len(result) != 0:
            #pdb.set_trace()
            response = auth_user(result[0]['email'], method, **kwargs)
            return response

        else:
            query = """ INSERT INTO "user" 
            (email, name, password, api_key,
                created_ts, first_name, last_name)
            VALUES ('{0}', '{1}', '{2}', '{3}',
                '{4}', '{5}', '{6}')""".format(
                email, username, password, api_key,
                created_ts, first_name, last_name)

            cursor.execute(query)
            postgre.commit()

            return json.dumps({'status': 'success','message': 'user added through facebook'})

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
        result = cursor.fetchall()

        # Email Password combination does not match
        if len(result) == 0:
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
                'user_id': result[0]['user_id'],
                'username': result[0]['name']
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
            response = {'status':'success','message':'user exists, logged in through signup fb'}
            return response


def user_follows_user(user_id, api_key, user_id_to_follow):
    '''
    When a user follows another user
    '''

    response = {}

    query = """ INSERT INTO "user_following" (user_id, follows_user_id) 
                VALUES ('{0}', '{1}') """.format(user_id, user_id_to_follow)

    cursor.execute(query)
    postgre.commit()

    response.update({
        'status':'success',
        'message':'User {0} is now following User {1}'.format(user_id,
                                                        user_id_to_follow)
    })

    return response