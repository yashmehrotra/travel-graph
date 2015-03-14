import os

from flask import Flask, request, Response
from flask import render_template, url_for, redirect, send_from_directory
from flask import send_file, make_response, abort

from travelgraph import app

# routing for basic pages (pass routing onto the Angular app)
@app.route('/')
@app.route('/login')
@app.route('/blog')
def basic_pages(**kwargs):
        return make_response(open('travelgraph/templates/index.html').read())

# from flask import render_template, session
# import pdb
# import json

# from travelgraph import app
# from travelgraph.apps.models import models_questions, models
# from travelgraph.apps.auth import login_required
# from travelgraph.apps.api.api_users import api_logout     # This line should be removed later on


# @app.route('/')
# def page_login():
#     return render_template('login.html')


# @app.route('/signup')
# def page_signup():
#     return render_template('signup.html')


# @app.route('/medium')
# def editor():
#     return render_template('med.html')


# @app.route('/cs')
# def cs():
#     return session['username']+session['api_key']


# @app.route('/ques')
# @login_required
# def ques():
#     return render_template('question.html')


# @app.route('/ques/<ques_id>/')
# @login_required
# def ques_id(ques_id):
#     question_details = models_questions.get_question(ques_id)
#     asker_details = models.user_details(question_details['user_id'])

#     data = {
#         'question': question_details,
#         'user': asker_details,
#     }

#     return render_template('QnA.html', data=data)
    

# @app.route('/user/<user_id>/')
# @login_required
# def user_id(user_id):
#     # data = models_questions.get_question(ques_id)
    
#     return render_template('user_profile.html')


# @app.route('/logout')
# @login_required
# def logout():
#     resp = api_logout()
#     return resp


    
# # @app.route('/qna')
# # def questions_n_answers():
#     # return render_template('QnA.html')

    
