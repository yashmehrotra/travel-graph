from ghoom.models import (
    engine,
    Base,
    DbType,
    DbTagType,
    Session
)

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
