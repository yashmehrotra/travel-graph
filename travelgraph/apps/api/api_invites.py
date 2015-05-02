from flask import request, session, jsonify
import hashlib
import json
import pdb

from travelgraph import app, settings
from travelgraph.apps.invites import models


@app.route('/invite/request/', methods=['POST'])
def request_invite():
    '''
    When a user requests for an invite
    '''

    email = request.form['email']

    response = models.add_email(email)

    return jsonify(response)


@app.route('/invite/accept/', methods=['POST'])
def accept_invite():
    '''
    When admin accepts user's invite
    '''

    email = request.form['email']

    response = models.invite_user(email)

    return jsonify(response)


@app.route('/invite/get_emails/', methods=['GET'])
def get_allowed_emails():
    '''
    Send a list of allowed emails for signup
    '''

    vip_list = models.get_all_emails(allowed=True)

    vip_list = [ vip['email'] for vip in vip_list ]

    response = {
        'status': 'success',
        'vip_list': vip_list,
    }

    return jsonify(response)
