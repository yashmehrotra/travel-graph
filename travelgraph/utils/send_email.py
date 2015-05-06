import mandrill

# Make a settings folder and add everything there

html_tag = ''
html_follower = ''
html_answer = ''
html_question_added = ''

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
