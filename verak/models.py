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
    String,
)

from sqlalchemy.event import listen

from verak.settings import SQLALCHEMY_ENGINE

Base = declarative_base()
engine = create_engine(SQLALCHEMY_ENGINE)
scoper = sessionmaker(bind=engine)
session = scoped_session(sessionmaker(bind=engine))

PK_KWARGS = {
    'autoincrement': True,
    'primary_key': True,
    'index': True,
    'unique': True
}


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

    id = Column(BigInteger, **PK_KWARGS)
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
            'profile_photo': self.profile_photo,
            'bio': self.bio,
            'create_ts': str(self.create_ts)
        }

        return user_dict


class DbType(Base):
    """
    The db_type table
    Will be like
    =================================
    | id  |  name    | tablename    |
    ---------------------------------
    |   1 | question | db_question  |
    |   2 | answer   | db_answer    |
    |   3 | blog     | db_blog      |
    =================================
    """

    __tablename__ = "db_type"

    id = Column(Integer, **PK_KWARGS)
    name = Column(String)
    tablename = Column(String)


class DbDoobieMapping(Base):
    """
    The db_doobie_mapping
    """

    __tablename__ = "db_doobie_mapping"

    id = Column(BigInteger, **PK_KWARGS)
    type_id = Column(Integer, ForeignKey(DbType.id))
    mapping_id = Column(BigInteger, index=True)

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


class DbQuestion(Base):
    """
    The db_question table
    """

    __tablename__ = "db_question"

    id = Column(BigInteger, **PK_KWARGS)
    title = Column(Unicode)
    description = Column(UnicodeText())
    user_id = Column(BigInteger, ForeignKey(DbUser.id), index=True)
    doobie_id = Column(BigInteger, ForeignKey(DbDoobieMapping.id), index=True)
    create_ts = Column(DateTime, default=datetime.now())
    update_ts = Column(DateTime, default=datetime.now())
    enabled = Column(Boolean, default=True)

    # user = relationship('DbUser', foreign_keys='DbQuestion.user_id')
    user = relationship(DbUser)
    doobie = relationship(DbDoobieMapping)

    @property
    def serialize(self):
        """
        The basic serializer
        """

        question_dict = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'user': self.user.serialize,
            'doobie_id': self.doobie_id,
            'tags': self.tags,
            'type': 'question'
        }

        return question_dict

    @property
    def type(self):
        """
        Returns the corresponding
        DbType Object
        """

        db_type_obj = session.query(DbType).\
                        filter(DbType.tablename == self.__tablename__).\
                        first()

        return db_type_obj

    @property
    def tags(self):
        """
        Returns a list of tags attached
        to the corresponding question
        """

        tag_mapping = session.query(DbDoobieTagMapping).\
                        filter(DbDoobieTagMapping.doobie_id == self.doobie_id,
                               DbDoobieTagMapping.enabled == True)

        tag_list = []

        if tag_mapping.count() > 0:
            tag_list = [mapping.tag.serialize
                        for mapping in tag_mapping]

        return tag_list


class DbAnswer(Base):
    """
    The db_answer table
    """

    __tablename__ = "db_answer"

    id = Column(BigInteger, **PK_KWARGS)
    answer = Column(UnicodeText)
    question_id = Column(BigInteger, ForeignKey(DbQuestion.id), index=True)
    user_id = Column(BigInteger, ForeignKey(DbUser.id), index=True)
    doobie_id = Column(BigInteger, ForeignKey(DbDoobieMapping.id), index=True)
    create_ts = Column(DateTime, default=datetime.now())
    update_ts = Column(DateTime, default=datetime.now())
    enabled = Column(Boolean, default=True)

    # question = relationship('DbQuestion', foreign_keys='DbAnswer.question_id')
    # user = relationship('DbUser', foreign_keys='DbAnswer.user_id')

    question = relationship(DbQuestion)
    user = relationship(DbUser)
    doobie = relationship(DbDoobieMapping)

    @property
    def serialize(self):
        """
        The basic answer serializer
        """

        answer_dict = {
            'id': self.id,
            'answer': self.answer,
            'question': self.question.serialize,
            'user': self.user.serialize,
            'create_ts': str(self.create_ts),
            'doobie_id': self.doobie_id,
            'tags': self.tags,
            'type': 'answer'
        }

        return answer_dict

    @property
    def tags(self):
        """
        Returns a list of all the tags
        corresponding to the answer
        """

        tag_mapping = session.query(DbDoobieTagMapping).\
                        filter(DbDoobieTagMapping.doobie_id == self.doobie_id,
                               DbDoobieTagMapping.enabled == True)

        tag_list = []

        if tag_mapping.count() > 0:
            tag_list = [mapping.tag.serialize
                        for mapping in tag_mapping]

        return tag_list


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

    id = Column(BigInteger, **PK_KWARGS)
    name = Column(Unicode, unique=True)
    type_id = Column(Integer, ForeignKey(DbTagType.id))
    create_ts = Column(DateTime, default=datetime.now())
    update_ts = Column(DateTime, default=datetime.now())
    enabled = Column(Boolean, default=True)

    type = relationship(DbTagType)

    @property
    def serialize(self):
        """
        Returns basic serializer
        """

        tag_dict = {
            'id': self.id,
            'tag': self.name
        }

        return tag_dict


class DbDoobieTagMapping(Base):
    """
    The db_doobie_tag_mapping table
    """

    __tablename__ = "db_doobie_tag_mapping"

    id = Column(BigInteger, **PK_KWARGS)
    doobie_id = Column(BigInteger, ForeignKey(DbDoobieMapping.id), index=True)
    tag_id = Column(BigInteger, ForeignKey(DbTag.id), index=True)
    # Think about below line, how to query, and how to insert
    tag_name = Column(Unicode)
    create_ts = Column(DateTime, default=datetime.now())
    update_ts = Column(DateTime, default=datetime.now())
    enabled = Column(Boolean, default=True)

    doobie_mapping = relationship(DbDoobieMapping)
    tag = relationship(DbTag)

    @property
    def doobie(self):
        """
        Returns the corresponding
        doobie object
        """

        return self.doobie_mapping.doobie


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

    id = Column(BigInteger, **PK_KWARGS)
    follower_id = Column(BigInteger, ForeignKey(DbUser.id), index=True)
    following_id = Column(BigInteger, ForeignKey(DbUser.id), index=True)
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

    id = Column(BigInteger, **PK_KWARGS)
    user_id = Column(BigInteger, ForeignKey(DbUser.id), index=True)
    tag_id = Column(BigInteger, ForeignKey(DbTag.id), index=True)
    # Think about below line, how to query, and how to insert and whether to add index=True
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

    id = Column(BigInteger, **PK_KWARGS)
    request_key = Column(String)
    type = Column(String)
    ttl = Column(BigInteger)


class DbEmailInvite(Base):
    """
    The db_email_invite table
    """

    __tablename__ = "db_email_invite"

    id = Column(BigInteger, **PK_KWARGS)
    email = Column(Unicode)
    invited = Column(Boolean, default=False)


class DbRole(Base):
    """
    The db_role table
    """

    __tablename__ = "db_role"

    id = Column(BigInteger, **PK_KWARGS)
    role = Column(String)


class DbRoleUserMapping(Base):
    """
    The db_role_user_mapping table
    """

    __tablename__ = "db_role_user_mapping"

    id = Column(BigInteger, **PK_KWARGS)
    role_id = Column(BigInteger, ForeignKey(DbRole.id), index=True)
    user_id = Column(BigInteger, ForeignKey(DbUser.id), index=True)
    create_ts = Column(DateTime, default=datetime.now())

    role = relationship(DbRole)
    user = relationship(DbUser)


# Define all event listensers and related stuff in the end
def map_doobie(mapper, connection, target):
    """
    This function maps all doobies in the
    db_doobie_mapping table
    """
    # Declare a temp session
    temp_sess = scoped_session(sessionmaker(bind=engine))

    tablename = target.__tablename__
    db_type = temp_sess.query(DbType).\
                filter(DbType.tablename == tablename).\
                first()

    doobie_mapping = DbDoobieMapping(type_id=db_type.id,
                                     mapping_id=target.id)

    temp_sess.add(doobie_mapping)

    temp_sess.commit()

    doobie_id = doobie_mapping.id
    temp_sess.close()

    doobie_table = get_class_by_tablename(tablename).__table__

    connection.execute(
            doobie_table.update().
            where(doobie_table.c.id == target.id).
            values(doobie_id=doobie_id)
    )


# Event Listeners
listen(DbQuestion, 'after_insert', map_doobie)
listen(DbAnswer, 'after_insert', map_doobie)
