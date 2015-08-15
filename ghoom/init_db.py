import sys
import os
sys.path.append(os.path.realpath('.'))

from ghoom.models import (
    engine,
    Base,
    DbType,
    DbTagType,
    session
)

from ghoom import app
from flask.ext.script import Manager

manager = Manager(app)


@manager.command
def create_db():

    Base.metadata.create_all(engine)
    print "All Tables Created Successfully"

    # Adding Doobie Types
    doobie_types = [DbType(name='question', tablename='db_question'),
                    DbType(name='answer', tablename='db_answer')]

    session.add_all(doobie_types)
    session.commit()

    # Adding Doobie Tag Types
    doobie_tag_types = [DbTagType(name='place'),
                        DbTagType(name='activity')]

    session.add_all(doobie_tag_types)
    session.commit()

    session.close()
    print 'Types and tag types added in DB'


@manager.command
def test():
    print 'Testing Stuff and imports'


if __name__ == "__main__":
    manager.run()
