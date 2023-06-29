from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DATE
from .connection import engine

Base = declarative_base()

class Produit(Base):
    __tablename__ = "produits"
    id = Column(Integer, primary_key=True, nullable=False)
    nom = Column(String(25), unique=True)
    date_fabrique = Column(DATE)
    date_expiration = Column(DATE)


class User(Base):
    __tablename__="users"
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(50), unique=True)
    password = Column(String(255))
    fullname = Column(String(100))



Base.metadata.create_all(bind=engine)