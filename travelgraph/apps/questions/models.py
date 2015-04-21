import json
from datetime import datetime
import pdb

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker

from sqlalchemy import event
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import BigInteger
from sqlalchemy import Unicode
from sqlalchemy import UnicodeText
from sqlalchemy import ForeignKey
from sqlalchemy import Table
from sqlalchemy import select

from sqlalchemy import create_engine

from travelgraph.apps.doobies.models import DoobieType
from travelgraph.apps.doobies.models import Doobie

from travelgraph.apps.tags.models import DoobieTagsMapping
from travelgraph.apps.tags.models import Tags

SQLALCHEMY_ENGINE = 'postgresql://yash:44rrff@localhost:5432/'
DATABASE = 'G2'

Base = declarative_base()
engine = create_engine(SQLALCHEMY_ENGINE+DATABASE)
Session = sessionmaker(bind=engine)

session = Session()

class Questions(Base):
    '''
    The doobie_questions table
    '''

    __tablename__ = "Questions"
    
    DOOBIE_NAME = "questions"
    
    doobie_type = DoobieType.get_doobie_type(DOOBIE_NAME)

    
    question_id = Column(BigInteger, autoincrement=True, primary_key=True)
    title       = Column(UnicodeText())
    description = Column(UnicodeText())
    user_id     = Column(BigInteger, primary_key=True)
    created_ts  = Column(DateTime, default=datetime.now())
    updated_ts  = Column(DateTime, default=datetime.now())

    @staticmethod
    def add_question(title, description, user_id, tags):
        ##
        ## Map tags to doobie , think how
        ##
        '''
        Add question
        '''

        response = {}

        question = Questions(title=title, description=description, user_id=user_id)

        session.add(question)
        session.commit()

        change_var_name = DoobieType.map_doobie(doobie_type, mapping_id)

        # Mapping Tags to Doobie
        doobie_type = Questions.doobie_type
        mapping_id = question.question_id
        # Make sure tags are in a unicoded list
        for tag in tags:
            DoobieTagsMapping.map_tag_to_doobie(tag, doobie_type, mapping_id)

        response = {
            'question_id': question.question_id,
            'title': question.title,
            'description': question.description,
            'user_id': question.user_id,
            'created_ts': question.created_ts,
            'updated_ts': question.updated_ts,
            'tags': DoobieTagsMapping.get_doobie_tags(doobie_type, mapping_id),
        }

        return response


    @staticmethod
    def get_question(question_id):
        '''
        Retrieve the question details through question_id
        '''

        ###
        ### RAISE ERROR IF QUESTION NOT FOUND OR SOMETHING
        ###

        question = session.query(Question).\
                           filter(Question.question_id==question_id).\
                           first()

        question_data = {
            'question_id': question.question_id,
            'title': question.title,
            'description': question.description,
            'user_id': question.user_id,
            'created_ts': question.created_ts,
            'updated_ts': question.updated_ts,
            'tags': DoobieTagsMapping.get_doobie_tags(doobie_type,
                                                    question.question_id),
        }

        return question_data


    @staticmethod
    def get_user_questions(user_id):
        '''
        Get all of the user's questions
        '''

        response = {
            'questions': [],
        }

        question_ids = session.query(Question.c.question_id).\
                           filter(Question.user_id == user_id)

        for id in question_id:
            response['questions'].append(Question.get_question(id))  # See if it works like this ie. inner method can be called

        response.update({
            'status': 'success',
            'message': 'add message',
        })

        return response


    @staticmethod
    def view_tag_questions(tag):
        '''
        Get all the questions corresponding to a particular tag
        '''

        response = {
            'questions': [],
        }

        tagged_doobies = Tags.get_tagged_doobies({
                        'tag': tag,
                        'doobie_type': Question.doobie_type,
                    })

        for question in tagged_doobies['doobies']:
            response['questions'].append(Question.get_question(
                                    question['mapping_id']))

        response.update({
            'status': 'success',
            'message': 'add message',
        })

        return response
