from flask import request, session, jsonify
import hashlib
import json
import pdb

from travelgraph import app, settings
from travelgraph.apps import auth

from travelgraph.apps.models import (
        models,
        models_questions,
        models_tags,
        models_answers
    )
from travelgraph.apps import user_session


@app.route('/api/content/add_question', methods=['POST'])
def api_add_question():
    '''
    The question details should be added
    '''
    question_title = request.form.get('question_title')
    question_desc  = request.form.get('question_desc')
    question_tags  = request.form.get('question_tags')

    # Take user id and api key from form first then session
    user_id = request.form.get('user_id', session.get('user_id'))

    result = models_questions.add_question(user_id, question_title,
                                question_desc, question_tags)

    return jsonify(result)


@app.route('/api/content/view_tag/<tag>', methods=['GET'])
def view_tagged_ques(tag):
    '''
    Display a list of all the questions related to the tag given
    '''
    if '-' in tag:
        tag = tag.split('-')
    result = models_questions.view_tagged_questions(tag)

    return jsonify(result)


@app.route('/api/content/view_all_ques', methods=['GET'])
def view_all_ques():
    '''
    Display a list of all the questions
    '''

    result = models_questions.view_all_questions()

    return jsonify(result)


@app.route('/api/tag/subscribe_tag', methods=['POST'])
def subscribe_tag():
    '''
    User wants to subscribe to a tag
    '''

    user_id = request.form.get('user_id', session.get('user_id'))
    tag     = request.form.get('tag')

    tag_id = models_tags.get_tag_id(tag)

    result = models_tags.user_subscribes_tag(user_id, tag_id)

    return jsonify(result)


@app.route('/api/user/follow_user', methods=['POST'])
def follow_user():
    '''
    User wants to follow another user
    '''

    user_id = request.form.get('user_id', session.get('user_id'))

    user_id_to_follow = request.form.get('user_id_to_follow')

    result = models.user_follows_user(user_id, user_id_to_follow)

    return jsonify(result)


@app.route('/api/content/add_answer', methods=['POST'])
def add_answer():
    '''
    Adding answer for a question
    '''

    user_id = request.form.get('user_id', session.get('user_id'))

    question_id = request.form.get('question_id')
    answer = request.form.get('answer')
    answer_tags = request.form.get('answer_tags')

    result = models_answers.add_answer(question_id, answer,
                                        answer_tags, user_id)

    return jsonify(result)


@app.route('/api/content/get_answers/<question_id>/')
def get_answers(question_id):
    '''
    Retrieving all the answers for a given question
    '''

    result = models_answers.get_all_answers(question_id)

    return jsonify(result)


@app.route('/api/content/get_question/<question_id>/')
def get_question(question_id):
    '''
    Retrieve a question with a given id
    '''

    result = models_questions.get_question(question_id)

    return jsonify(result)


@app.route('/api/content/get_user_questions/<user_id>/')
def get_all_user_questions(user_id):
    '''
    Retrieve a question with a given id
    '''

    result = models_questions.get_user_questions(user_id)

    return jsonify(result)


@app.route('/api/content/follow_question', methods=['POST'])
def subscribe_question():
    '''
    User wants to subscribe to a question with question_id given
    '''

    user_id = request.form.get('user_id')
    question_id = request.form.get('question_id')

    result = models_questions.subscribe_question(question_id, user_id)

    return jsonify(result)


@app.route('/api/content/followed_questions/<user_id>', methods=['GET'])
def list_followed_questions(user_id):
    '''
    Return a list of followed questions
    '''

    result = models_questions.get_followed_questions(user_id)

    return jsonify(result)
