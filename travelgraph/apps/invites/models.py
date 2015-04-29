import pdb
import json
import hashlib
import random
from datetime import datetime

from travelgraph import settings
from travelgraph.apps.database import postgre, cursor


def add_email(email):
    '''
    When a user requests for an invite
    '''

    response = {}

    if not check_duplicate(email):

        query = """ INSERT INTO "email_invite" 
                    (email) VALUES ('{0}') """.format(email)

        cursor.execute(query)
        postgre.commit()

        send_email_admin(email)

        response.update({
            'status': 'success',
            'email': email,
        })
    
    else:
        response.update({
            'status': 'failed',
            'email': email,
            'error': 'Email already sent for invite'
        })

    return response


def send_email_admin(email):
    '''
    Send user's invite request to admin
    '''
    pass


def get_all_emails(allowed=False):
    '''
    Get list of allowed emails for signup
    '''

    if allowed:
        query = """ SELECT * FROM "email_invite" WHERE allowed = '1' """
    else:
        query = """ SELECT * FROM "email_invite" """

    cursor.execute(query)
    result = cursor.fetchall()

    vip_list = []

    for row in result:
        vip_list.append({
            'email': row['email'],
            'allowed': row['allowed'],
        })

    return vip_list


def invite_user(email):
    '''
    Admin says that this user can be invited
    '''
    
    query = """ UPDATE "email_invite"
                SET allowed = '1'
                WHERE email = '{0}' """.format(email)

    response = {
        'status': 'success',
        'message': 'user invited',
    }

    return response

def send_email_user():
    '''
    Send email to user stating he can signup
    '''
    pass


def check_duplicate(email):
    '''
    Returns true if duplicates exists
    False otherwise
    '''

    vip_list = get_all_emails(email)

    for row in vip_list:
        if email == row['email']:
            return True

    return False
