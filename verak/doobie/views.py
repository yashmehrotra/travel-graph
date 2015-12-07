from flask import Blueprint, request
from flask.views import MethodView
from datetime import datetime

from verak.models import (
    DbAnswer,
    DbQuestion,
    session
)
from verak.decorators import (
    auth_required,
    login_required
)

from verak.helpers import (
    response_json,
    response_error
)

from verak.search.tasks import index_es
from verak.tag.tasks import map_tags_to_doobie

api_question = Blueprint('api_question', __name__)


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

        # Make it efficient
        answers = session.query(DbAnswer).\
                    filter(DbAnswer.question_id == question_id).\
                    all()
        # Below is temp
        ans = []
        for answer in answers:
            ans.append(answer.serialize)
        resp = {
            'status': 'success',
            'answers': ans,
            'question': question.serialize
        }
        return response_json(resp)

    elif request.method == 'GET' and not question_id:
        """
        Currently returns a list of all questions
        """
        questions = session.query(DbQuestion).\
                        order_by(DbQuestion.id.desc()).all()

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
            tags = tags.split(',') if type(tags) != list else tags
            map_tags_to_doobie(tags, question.doobie_id)

        index_es(question)

        response = {
            'status': 'success',
            'question': question.serialize
        }

        return response_json(response)

    elif request.method == 'PUT' and question_id:
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
        question.update_ts = datetime.now()

        session.commit()

        # Below is temp
        # Mappings enabled flag will be turned to false for deleted tags
        if tags:
            # TODO: Handle edit question, add new tags, disable old mapping
            tags = tags.split(',') if type(tags) != list else tags
            map_tags_to_doobie(tags, question.doobie_id)

        index_es(question)
        return response_json(question.serialize)


class ApiAnswerView(MethodView):
    """
    Return a specific answer based on the used
    """

    url_endpoint = [
        {'url': '/<int:question_id>/answer/',
         'methods': ['GET', 'POST']},
        {'url': '/<int:question_id>/answer/<int:user_id>/',
         'methods': ['GET', 'PUT']}
    ]
    blueprint = api_question
    decorators = [auth_required, login_required]

    def post(self, question_id=None):
        if not question_id:
            return response_error('question_id not provided')

        answer_text = request.form.get('answer')
        tags = request.form.get('tags')

        if not answer_text:
            return response_error('answer should be provided')

        user_id = request.user_id

        # Check if user hasn't already answered the question
        # TODO: Use sqlalchemy's exists here
        user_ans_count = session.query(DbAnswer).\
                            filter(DbAnswer.question_id == question_id,
                                   DbAnswer.user_id == user_id).\
                            count()

        if user_ans_count > 0:
            return response_error('User already has answered this question')

        answer = DbAnswer(answer=answer_text,
                          question_id=question_id,
                          user_id=user_id)

        session.add(answer)
        session.commit()

        if tags:
            tags = tags.split(',') if type(tags) != list else tags
            map_tags_to_doobie(tags, answer.doobie_id)

        index_es(answer)

        response = {
            'status': 'success',
            'message': 'Answer successfully added',
            'answer': answer.serialize
        }

        return response_json(response)

    def get(self, question_id=None, user_id=None):

        if not question_id:
            return response_error('question_id not provided')

        answer = session.query(DbAnswer).\
                    filter(DbAnswer.question_id == question_id)

        if user_id:
            answer = answer.filter(DbAnswer.user_id == user_id).\
                        first()

            response = {
                'status': 'success',
                'answer': answer.serialize
            }

        else:
            answer = answer.all()

            response = {
                'status': 'success',
                'answers': [a.serialize for a in answer]
            }

        return response_json(response)

    def put(self, question_id=None, user_id=None):

        if not user_id:
            return response_error('user_id not provided')

        if not question_id:
            return response_error('question_id not provided')

        answer = session.query(DbAnswer).\
                    filter(DbAnswer.question_id == question_id,
                           DbAnswer.user_id == user_id).\
                    first()

        if not answer:
            return response_error('User has not yet answered the question')

        answer_text = request.form.get('answer')
        tags = request.form.get('tags')

        if not answer_text:
            return response_error('Answer should be provided')

        answer.answer = answer_text
        answer.update_ts = datetime.now()

        session.commit()

        # TODO: Handle what happens to tags which are delisted
        if tags:
            tags = tags.split(',') if type(tags) != list else tags
            map_tags_to_doobie(tags, answer.doobie_id)

        index_es(answer)

        response = {
            'status': 'success',
            'message': 'Answer succesfully edited',
            'answer': answer.serialize
        }

        return response_json(response)
