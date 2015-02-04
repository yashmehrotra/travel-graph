from flask import render_template, session
import pdb
import json

from travelgraph import app
from travelgraph.apps.models import models_questions
from travelgraph.apps.auth import login_required
from travelgraph.apps.api.api_users import api_logout     # This line should be removed later on


@app.route('/')
def page_login():
    return render_template('login.html')


@app.route('/signup')
def page_signup():
    return render_template('signup.html')


@app.route('/medium')
def editor():
    return render_template('med.html')


@app.route('/cs')
def cs():
    return session['username']+session['api_key']


@app.route('/ques')
@login_required
def ques():
    return render_template('question.html')


@app.route('/ques/<ques_id>/')
@login_required
def ques_id(ques_id):
    data = models_questions.get_question(ques_id)
    return render_template('ques_id.html', data=data)


@app.route('/logout')
@login_required
def logout():
    resp = api_logout()
    return resp
