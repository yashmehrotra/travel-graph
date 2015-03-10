import json
from datetime import datetime
import pdb
import hashlib

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
from sqlalchemy import func

from sqlalchemy import create_engine

SQLALCHEMY_ENGINE = 'postgresql://yash:44rrff@localhost:5432/'
DATABASE = 'G2'

Base = declarative_base()
engine = create_engine(SQLALCHEMY_ENGINE+DATABASE)
Session = sessionmaker(bind=engine)

session = Session()

class Users(Base):
    '''
    The main user class
    '''

    __tablename__ = "Users"

    user_id       = Column(BigInteger, autoincrement=True, primary_key=True)
    username      = Column(UnicodeText())
    email         = Column(String(420))
    password      = Column(String(420))
    first_name    = Column(UnicodeText())
    last_name     = Column(UnicodeText())
    profile_photo = Column(UnicodeText())
    bio           = Column(UnicodeText())
    created_ts    = Column(DateTime, default=datetime.now())
    updated_ts    = Column(DateTime, default=datetime.now())
    login_ts      = Column(DateTime, default=datetime.now())

    #think of creating a new table
    facebook_token = Column(UnicodeText())
    google_token   = Column(UnicodeText())


    @staticmethod
    def create_user(**params):
        '''
        Create a user here
        params - email, first_name, last_name, password, bio
        DO NOT ENCODE EMAIL
        '''

        response = {}

        try:

            # To check whether the user exists or not
            user_exists = session.query(Users).filter(Users.email == email)

            # If he exists
            if user_exists:
                response.update({
                    'status':'failed',
                    'error':'A user with the same email already exists',
                })

                return response

            username = Users._generate_username(params['first_name'],params['last_name'])

            password = params.get('password',Users._get_random_word(12))
            password = hashlib.sha256(password).hexdigest()

            user = Users(username=username,
                         email=params['email'],
                         password=password,
                         first_name=params['first_name'],
                         last_name=params['last_name'],
                         bio=params['bio'])

            session.add(user)
            session.commit()

            response.update({
                'status': 'success',
                'message': 'add message',
                'user': {
                    'user_id': user.user_id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'bio': user.bio,
                }
            })

        except KeyError:
            # do something here
            # send failed
            pass

        except Exception as inst:
            raise(inst) # Check if syntax is right

        finally:
            return response


    @staticmethod
    def _generate_username(first_name, last_name):
        '''
        Generate a person's username using first and last name
        '''

        username = u'{0}-{1}-'.format(first_name.lower(), last_name.lower())

        count = session.query(Users).\
                        filter(Users.firt_name.lower() == firt_name.lower(),
                               Users.last_name.lower() == last_name.lower()).\
                        count()

        username += unicode(count)

        return username


    @staticmethod
    def get_random_word(wordLen):
        word = ''
        for i in range(wordLen):
            word += random.choice(('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrs'
                                   'tuvwxyz0123456789/&='))

        word = unicode(word,'utf-8')
        return word


    @staticmethod
    def validate_user(**params):
        '''
        Validate email and password
        '''

        response = {}

        method = params['method']
        email = params['email']

        query = session.query(Users).\
                        filter(Users.email == email).\
                        first()

        if method == 'normal':
            password = params['password']
            password = hashlib.sha256(password).hexdigest()
            # Get user id and validate

            if query.password == password:
                response.update({
                    'status': 'success',
                })
                
            else:
                # Error Response

        elif method == 'facebook':
            # Get user id and validate
