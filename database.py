from sqlalchemy import create_engine #database er shathe connect korte
from sqlalchemy.orm import sessionmaker #database er jonno session create korbe
from sqlalchemy.ext.declarative import declarative_base #

engine = create_engine("sqlite:///todo.db") #pyhon er jonno builtin database

Base = declarative_base() #instance create inherit from declarative base

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False) 