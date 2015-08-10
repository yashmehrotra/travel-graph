import sys,os
sys.path.append(os.path.realpath('.'))

from ghoom.models import (
    engine,
    Base,
    DbType,
    DbTagType,
    Session
)
from __init__ import app
from flask.ext.script import Manager

manager = Manager(app)

@manager.command
def test():
    print 'stuff'

if __name__ == "__main__":
    manager.run()
"""
Base.metadata.create_all(engine)

session = Session()
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
"""
