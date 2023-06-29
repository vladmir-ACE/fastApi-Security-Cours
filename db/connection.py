from sqlalchemy import create_engine
from sqlalchemy.dialects.sqlite import *
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args = {"check_same_thread": False})

SECRET_KEY = "dhbfekbjwfvkjcvhkjjbdsaugfdfk"

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

