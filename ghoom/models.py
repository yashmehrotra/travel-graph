from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    relationship,
    sessionmaker
)

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    BigInteger,
    Unicode,
    UnicodeText,
    ForeignKey,
)

Base = declarative_base()
Session = sessionmaker(bind=engine)

session = Session()


def get_class_by_tablename(tablename):
    """
    Return class reference mapped to table.
    :param tablename: String with name of table.
    :return: Class reference or None.
    """
    for c in Base._decl_class_registry.values():
        if hasattr(c, '__tablename__') and c.__tablename__ == tablename:
            return c


class DbUser(Base):
    """
    The db_user table
    """

    __tablename__ = "db_user"

    def __init__(self, *args, **kwargs):
        # Overide to generate username
        pass

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    username = Column(Unicode)
    email = Column(Unicode)
    first_name = Column(Unicode)
    last_name = Column(Unicode)
    password = Column(Unicode)
    profile_photo = Column(Unicode)
    bio = Column(UnicodeText())
    create_ts = Column(DateTime, default=datetime.now())
    update_ts = Column(DateTime, default=datetime.now())
    login_ts = Column(DateTime, default=datetime.now())
    facebook_token = Column(UnicodeText())
    google_token = Column(UnicodeText())


class DbQuestion(Base):
    """
    The db_question table
    """

    __tablename__ = "db_question"

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    title = Column(Unicode)
    description = Column(UnicodeText())
    user_id = Column(BigInteger, ForeignKey(DbUser.id), primary_key=True)
    create_ts = Column(DateTime, default=datetime.now())
    update_ts = Column(DateTime, default=datetime.now())
    enabled = Column(Boolean, default=True)

    # user = relationship('DbUser', foreign_keys='DbQuestion.user_id')
    user = relationship(DbUser)


class DbAnswer(Base):
    """
    The db_answer table
    """

    __tablename__ = "db_answer"

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    answer = Column(UnicodeText)
    question_id = Column(BigInteger, ForeignKey(DbQuestion.id), primary_key=True)
    user_id = Column(BigInteger, ForeignKey(DbUser.id), primary_key=True)
    create_ts = Column(DateTime, default=datetime.now())
    update_ts = Column(DateTime, default=datetime.now())
    enabled = Column(Boolean, default=True)

    # question = relationship('DbQuestion', foreign_keys='DbAnswer.question_id')
    # user = relationship('DbUser', foreign_keys='DbAnswer.user_id')

    question = relationship(DbQuestion)
    user = relationship(DbUser)


class DbType(Base):
    """
    The db_type table
    """

    __tablename__ = "db_type"

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Unicode)
    table_name = Column(Unicode)


class DbDoobieMapping(Base):
    """
    The db_doobie_mapping
    """
    pass
