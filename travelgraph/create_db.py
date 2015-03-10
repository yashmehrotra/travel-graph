from settings import SQLALCHEMY_ENGINE, DATABASE
from apps.tags.models import Base

from sqlalchemy import create_engine

engine = create_engine(SQLALCHEMY_ENGINE+DATABASE)
Base.metadata.create_all(engine)