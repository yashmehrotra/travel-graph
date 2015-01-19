from flask import render_template, session
import pdb

from travelgraph import app


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
def ques():
    return render_template('question.html')
