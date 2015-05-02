import pdb
import json
import hashlib
import random
from datetime import datetime
import mandrill

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
    
    html = """
            <p>
                Hello Ghoom Devta, this email {0} has requested for an
                invite. It is in your power to allow him to use the magic
                of Ghoom. Send a POST request with a email parameter 
                as this email to /invite/accept/.
            </p>
            """.format(email)

    subject = "Invite Requested for Ghoom"
    from_email = settings.GHOOM_EMAIL

    to = []
    
    for email in settings.ADMIN_EMAILS:
        to.append({
            'email': email,
            'name': 'Admin',
            'type': 'to'
        })

    from_name = 'Babaji'

    email_response = post_email(to,subject,from_email,from_name,html)

    return email_response



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

    cursor.execute(query)
    postgre.commit()

    send_email_user(email)

    response = {
        'status': 'success',
        'message': 'user invited',
    }

    return response

def send_email_user(email):
    '''
    Send email to user stating he can signup
    '''

    html = """
            <p>
                Hello fellow explorer, you have been invited to 
                join Ghoom's community. To signup, please use this 
                email - '{0} . Here is the <a href="http://www.ghoom.co/login">link</a>.'
            </p>
            """.format(email)

    subject = "Invitation for Ghoom"
    from_email = settings.GHOOM_EMAIL

    to = []
    
    to.append({
        'email': email,
        'name': 'Explorer',
        'type': 'to'
    })

    from_name = 'Babaji'

    email_response = post_email(to,subject,from_email,from_name,html)

    return email_response


def check_duplicate(email):
    '''
    Returns true if duplicates exists
    False otherwise
    '''

    vip_list = get_all_emails()

    for row in vip_list:
        if email == row['email']:
            return True

    return False


def post_email(to,subject,from_email,from_name,html):
    '''
    The generic email poster

    to example - [{
                    'email': 'ynmehrotra@gmail.com',
                    'name': 'Explorer',
                    'type': 'to'}]
    '''

    try:
        mandrill_client = mandrill.Mandrill(settings.MANDRILL_API_KEY)
        
        message = {
            'from_email': from_email,
            'from_name': from_name,
            'headers': {'Reply-To': from_email},
            'html': html,
            'images': None,
            'inline_css': None,
            'metadata': {'website': 'www.ghoom.co'},
            'subject': subject,
            'to': to,
            'view_content_link': None
         }
        
        result = mandrill_client.messages.send(message=message, async=False)
        
        '''
        [{'_id': 'abc123abc123abc123abc123abc123',
          'email': 'recipient.email@example.com',
          'reject_reason': 'hard-bounce',
          'status': 'sent'}]
        '''

        return result

    except Exception,e:
        # Mandrill errors are thrown as exceptions
        print 'A mandrill error occurred: %s - %s' % (e.__class__, e)
        # A mandrill error occurred: <class 'mandrill.UnknownSubaccountError'> - No subaccount exists with the id 'customer-123'    
        raise
