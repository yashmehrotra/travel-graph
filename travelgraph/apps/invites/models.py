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

	query = """  """
	cursor.execute(query)
	postgre.commit()

	send_email_admin(email)

	response.update({
		'status': 'success',
		'email': email,
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
		query = """ """

	pass


def invite_user(email):
	'''
	Admin says that this user can be invited
	'''
	pass

def send_email_user():
	'''
	Send email to user stating he can signup
	'''
	pass
