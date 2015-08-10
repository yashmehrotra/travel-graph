from sqlalchemy import create_engine

from ghoom.models import Base
from settings import SQLALCHEMY_ENGINE

engine = create_engine(SQLALCHEMY_ENGINE)
Base.metadata.create_all(engine)
