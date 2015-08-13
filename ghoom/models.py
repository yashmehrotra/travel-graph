from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    relationship,
    sessionmaker,
    scoped_session
)

from sqlalchemy import (
    create_engine,
    Boolean,
    Column,
    DateTime,
    Integer,
    BigInteger,
    Unicode,
    UnicodeText,
    ForeignKey,
    String
)

from ghoom.settings import SQLALCHEMY_ENGINE

Base = declarative_base()
engine = create_engine(SQLALCHEMY_ENGINE)
session = scoped_session(sessionmaker(bind=engine))


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

    @property
    def serialize(self):
        """
        Basic User Serializer
        """

        user_dict = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
        }

        return user_dict


class DbQuestion(Base):
    """
    The db_question table
    """

    __tablename__ = "db_question"

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    title = Column(Unicode)
    description = Column(UnicodeText())
    user_id = Column(BigInteger, ForeignKey(DbUser.id))
    create_ts = Column(DateTime, default=datetime.now())
    update_ts = Column(DateTime, default=datetime.now())
    enabled = Column(Boolean, default=True)

    # user = relationship('DbUser', foreign_keys='DbQuestion.user_id')
    user = relationship(DbUser)

    @property
    def serialize(self):
        """
        The basic serializer
        """

        question_dict = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'user': self.user.serialize
        }

        return question_dict


class DbAnswer(Base):
    """
    The db_answer table
    """

    __tablename__ = "db_answer"

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    answer = Column(UnicodeText)
    question_id = Column(BigInteger, ForeignKey(DbQuestion.id))
    user_id = Column(BigInteger, ForeignKey(DbUser.id))
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
    Will be like
    =================================
    | id  |  name    | table_name   |
    ---------------------------------
    |   1 | question | db_question  |
    |   2 | answer   | db_answer    |
    |   3 | blog     | db_blog      |
    =================================
    """

    __tablename__ = "db_type"

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)
    tablename = Column(String)


class DbDoobieMapping(Base):
    """
    The db_doobie_mapping
    """

    __tablename__ = "db_doobie_mapping"

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    type_id = Column(Integer, ForeignKey(DbType.id))
    mapping_id = Column(BigInteger)

    type = relationship(DbType)

    @property
    def doobie(self, *args, **kwargs):
        """
        Return the doobie object
        (Question/Answer/Blog)
        """

        tablename = self.type.tablename
        doobie_class = get_class_by_tablename(tablename)
        doobie_object = session.query(doobie_class).get(self.mapping_id)
        return doobie_object


class DbTagType(Base):
    """
    The db_tag_type table
    """

    __tablename__ = "db_tag_type"

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)


class DbTag(Base):
    """
    The db_tag table
    """

    # Override init to check for lower unique tag name
    __tablename__ = "db_tag"

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    name = Column(Unicode, unique=True)
    type_id = Column(Integer, ForeignKey(DbTagType.id))
    create_ts = Column(DateTime, default=datetime.now())
    update_ts = Column(DateTime, default=datetime.now())
    enabled = Column(Boolean, default=True)

    type = relationship(DbTagType)


class DbDoobieTagMapping(Base):
    """
    The db_doobie_tag_mapping table
    """

    __tablename__ = "db_doobie_tag_mapping"

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    doobie_id = Column(BigInteger, ForeignKey(DbDoobieMapping.id))
    tag_id = Column(BigInteger, ForeignKey(DbTag.id))
    # Think about below line, how to query, and how to insert
    tag_name = Column(Unicode, ForeignKey(DbTag.name))
    create_ts = Column(DateTime, default=datetime.now())
    update_ts = Column(DateTime, default=datetime.now())
    enabled = Column(Boolean, default=True)


class Following(object):
    """
    The parent following class
    """
    # Put Common Stuff Here
    pass


class DbUserFollowing(Base, Following):
    """
    The db_user_following table
    """

    __tablename__ = "db_user_following"

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    follower_id = Column(BigInteger, ForeignKey(DbUser.id))
    following_id = Column(BigInteger, ForeignKey(DbUser.id))
    create_ts = Column(DateTime, default=datetime.now())
    update_ts = Column(DateTime, default=datetime.now())
    enabled = Column(Boolean, default=True)

    follower = relationship('DbUser', foreign_keys='DbUserFollowing.follower_id')
    following = relationship('DbUser', foreign_keys='DbUserFollowing.following_id')


class DbUserTagFollowing(Base, Following):
    """
    The db_user_tag_following table
    """

    __tablename__ = "db_user_tag_following"

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    user_id = Column(BigInteger, ForeignKey(DbUser.id))
    tag_id = Column(BigInteger, ForeignKey(DbTag.id))
    # Think about below line, how to query, and how to insert
    tag_name = Column(Unicode, ForeignKey(DbTag.name))
    create_ts = Column(DateTime, default=datetime.now())
    update_ts = Column(DateTime, default=datetime.now())
    enabled = Column(Boolean, default=True)

    user = relationship(DbUser)
    tag = relationship('DbTag', foreign_keys='DbUserTagFollowing.tag_id')


class DbRequestKey(Base):
    """
    The db_request_key table
    """

    __tablename__ = "db_request_key"

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    request_key = Column(String)
    type = Column(String)
    ttl = Column(BigInteger)


class DbEmailInvite(Base):
    """
    The db_email_invite table
    """

    __tablename__ = "db_email_invite"

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    email = Column(Unicode)
    invited = Column(Boolean, default=False)


class DbRole(Base):
    """
    The db_role table
    """

    __tablename__ = "db_role"

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    role = Column(String)


class DbRoleUserMapping(Base):
    """
    The db_role_user_mapping table
    """

    __tablename__ = "db_role_user_mapping"

    id = Column(BigInteger, autoincrement=True, primary_key=True)
    role_id = Column(BigInteger, ForeignKey(DbRole.id))
    user_id = Column(BigInteger, ForeignKey(DbUser.id))
    create_ts = Column(DateTime, default=datetime.now())

    role = relationship(DbRole)
    user = relationship(DbUser)
