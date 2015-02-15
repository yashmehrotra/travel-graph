import hashlib
import psycopg2 as pgsql
import psycopg2.extras
from flask import session

from database import postgre, cursor


def create_session(email):
    
    query = """ SELECT * FROM "user"
        WHERE email = '{0}' """.format(email)

    cursor.execute(query)
    result = cursor.fetchone()

    session['user_id']    = result['user_id']
    session['username']   = result['username']
    session['email']      = result['email']
    session['first_name'] = result['first_name']
    session['last_name']  = result['last_name']

    print 'session created'


#No attributes cause we are destroying the current session
def destroy_session():
    session.clear()