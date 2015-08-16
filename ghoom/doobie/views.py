from flask import Blueprint, request
from datetime import datetime

from ghoom.models import (
    DbAnswer,
    DbQuestion,
    DbTag,
    session
)
from ghoom.decorators import (
    auth_required,
    login_required
)

from ghoom.helpers import (
    response_json,
    response_error
)

api_question = Blueprint('api_question', __name__)
api_answer = Blueprint('api_answer', __name__)


@api_question.route('/', methods=['GET', 'POST'])
@api_question.route('/<question_id>', methods=['GET', 'PUT'])
@auth_required
@login_required
def question_view(question_id=None):
    """
    Main question view
    """

    if request.method == 'GET' and question_id:

        question = session.query(DbQuestion).\
                    get(question_id)

        answers = session.query(DbAnswer).\
                    filter(DbAnswer.question_id == question_id)
        # Below is temp
        return response_json(question.serialize)

    elif request.method == 'GET' and not question_id:
        """
        Currently returns a list of all questions
        """
        questions = session.query(DbQuestion).all()

        response = {
            'status': 'success',
            'questions': []
        }

        for q in questions:
            response['questions'].append(q.serialize)

        return response_json(response)

    elif request.method == 'POST':
        """
        For adding a question
        """

        try:
            title = request.form['title']
            description = request.form.get('description')
            tags = request.form.get('tags')
        except KeyError:
            response_error("Missing parameters")

        # Change Below
        question = DbQuestion(title=title,
                              description=description,
                              user_id=request.user_id)

        session.add(question)
        session.commit()

        # Below is temp
        if tags:
            tags = tags.split(',')

        return response_json(question.serialize)

    elif request.method == 'PUT':
        """
        To Edit the given question
        """

        try:
            title = request.form['title']
            description = request.form.get('description')
            tags = request.form.get('tags')
        except KeyError:
            response_error("Missing parameters")

        question = session.query(DbQuestion).get(question_id)

        question.title = title
        question.description = description
        question.update_ts = datetime.now

        session.add(question)
        session.commit()

        # Below is temp
        # Mappings enabled flag will be turned to false for deleted tags
        if tags:
            tags = tags.split(',')

        return response_json(question.serialize)


@api_question.route('/<question_id>/answer')
@api_question.route('/<question_id>/answer/<user_id>')
@auth_required
@login_required
def answer_view(question_id=None, user_id=None):
    """
    Return a specific answer based on the used
    """

    if request.method == 'POST':
        if user_id:
            return response_error('user_id should not be provided')

        answer_text = request.form.get('answer')

        if not answer_text:
            return response_error('answer should be provided')

        user_id = request.user_id

        # Check if user hasn't already answered the question
        user_ans_count = session.query(DbAnswer).\
                            filter(DbAnswer.question_id == question_id,
                                   DbAnswer.user_id == user_id).\
                            count()

        if user_ans_count > 0:
            return response_error('User already has answered this question')

        answer = DbAnswer(answer=answer_text,
                          question_id=question_id,
                          user_id=user_id)

        session.add(user_id)
        session.commit()

        response = {
            'status': 'success',
            'message': 'Answer successfully added',
            'answer': answer.serialize
        }

        return response_json(response)

    elif request.method == 'GET':
        if not user_id:
            return response_error('user_id not provided')

        answer = session.query(DbAnswer).\
                    filter(DbAnswer.question_id == question_id,
                           DbAnswer.user_id == user_id).\
                    first()

        response = {
            'status': 'success',
            'answer': answer.serialize
        }

        return response_json(response)
