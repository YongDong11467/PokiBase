# Source: https://mysql.wisborg.dk/2019/03/03/using-sqlalchemy-with-mysql-8/

import mysql.connector
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

# Do not forget to install mysql.connector and sqlalchemy
# pip install mysql-connector-python

import connection_info

engine = sqlalchemy.create_engine(
    'mysql+mysqlconnector://root:' + connection_info.MyPassword + connection_info.MyHost + connection_info.MyDatabase,
    echo=True)

# Define and create the table
Base = declarative_base()

class StorePokemon(Base):

    __tablename__ = 'pokemon'

    pokemonid = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    pokemonname = sqlalchemy.Column(sqlalchemy.String(length=50))
    height = sqlalchemy.Column(sqlalchemy.Integer)
    weight = sqlalchemy.Column(sqlalchemy.Integer)

    def __init__(self, pokemonid, pokemonname, height, weight):
        self.pokemonid = pokemonid
        self.pokemonname = pokemonname
        self.height = height
        self.weight = weight

    def __repr__(self):
        return "<StorePokemon(pokemonid='{0}', pokemonname='{1}', height='{2}', weight='{3}')>".format(
            self.pokemonid, self.pokemonname, self.height, self.weight)

class StoreMoveRel(Base):

    __tablename__ = 'moverel'

    pokemonid = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    moveid = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)

    def __init__(self, pokemonid, moveid):
        self.pokemonid = pokemonid
        self.moveid = moveid

    def __repr__(self):
        return "<StoreMoveRel(pokemonid='{0}', moveid='{1}'>".format(
            self.pokemonid, self.moveid)

class StoreMove(Base):

    __tablename__ = 'move'

    moveid = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    typeid = sqlalchemy.Column(sqlalchemy.Integer)
    name = sqlalchemy.Column(sqlalchemy.String(length=50))
    description = sqlalchemy.Column(sqlalchemy.String(length=200))
    accuracy = sqlalchemy.Column(sqlalchemy.Integer)
    power = sqlalchemy.Column(sqlalchemy.Integer)

    def __init__(self, moveid, typeid, name, description, accuracy, power):
        self.moveid = moveid
        self.typeid = typeid
        self.name = name
        self.description = description
        self.accuracy = accuracy
        self.power = power

    def __repr__(self):
        return "<StoreMove(moveid='{0}', typeid='{1}', name='{2}', description='{3}', accuracy'{4}', power'{5}')>".format(
            self.moveid, self.typeid, self.name, self.description, self.accuracy, self.power)


Base.metadata.create_all(engine)  # creates the stores table

# Create a session
Session = sqlalchemy.orm.sessionmaker()
Session.configure(bind=engine)
session = Session()
