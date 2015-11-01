from sqlalchemy import create_engine

from hltv.models import Base

engine = create_engine('sqlite:///data.sqlite')

Base.metadata.create_all(engine)