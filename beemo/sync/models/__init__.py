from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql://liveslocal:liveslocal123@localhost/liveslocal')

# SQLAlchemy declarative base boilerplate
Base = declarative_base()
Base.metadata.bind = engine
Session = sessionmaker(bind=engine)

# Directory file imports
from .participant import RParticipant
