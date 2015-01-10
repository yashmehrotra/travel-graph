import psycopg2 as pgsql
import psycopg2.extras
import pdb
import json
import hashlib

from travelgraph import settings

'''
Types of methods - 
1.normal
2.facebook
3.google
4.twitter
'''


def init_pgsql_db(database=settings.pgsql_db):
    '''
    Initialize a server instance
    '''
    postgre = pgsql.connect(
            host=settings.pgsql_host,
            user=settings.pgsql_user,
            password=settings.pgsql_password,
            database=database,
        )

    return postgre


def create_user(email, method=None, **kwargs):
    '''
    This function adds user to the database
    '''
    ##
    ## We should also keep first name and last name in the database
    ##
    username = kwargs.get('first_name') + '-' + kwargs.get('last_name')

    password = hashlib.md5(kwargs.get('password')).hexdigest()

    # Add a function which sees how many users of the same name are there
    
    postgre = init_pgsql_db()
    cursor = postgre.cursor(cursor_factory=psycopg2.extras.DictCursor)

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
            (email, name, password) 
            VALUES ('{0}', '{1}', '{2}')""".format(email, username, password)

        cursor.execute(query)
        postgre.commit()

    elif method == 'facebook':
        
        # To see if user has already signed up and wants to login
        if len(result) != 0:
            auth_user(result[0]['email'], method='facebook')
        else:
            query = """ INSERT INTO "user" 
                (email, name, password) 
                VALUES ('{0}', '{1}', '{2}')""".format(email, username, password)

        cursor.execute(query)
        postgre.commit()

        return json.dumps({'status':'success','message':'user added through facebook'})
    
    return 'Done, also add exception here'


def auth_user(email, method=None, **kwargs):
    '''
    Sees whether info is correct
    '''
    postgre = init_pgsql_db()
    cursor = postgre.cursor(cursor_factory=psycopg2.extras.DictCursor)

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
                'status':'failed',
                'error':'Email password combination does not match'
            })

            return response

        else:
            # Start session here
            return result[0]['user_id']

    elif method == 'facebook':
        '''
        Login through Facebook
        ''' 
        
        query = """ SELECT * FROM "user"
            WHERE email = '{0}' """.format(email)