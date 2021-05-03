# Source: https://mysql.wisborg.dk/2019/03/03/using-sqlalchemy-with-mysql-8/

import mysql.connector
import sqlalchemy
from sqlalchemy import Index
from sqlalchemy.ext.declarative import declarative_base

# Do not forget to install mysql.connector and sqlalchemy
# pip install mysql-connector-python

import connection_info

engine = sqlalchemy.create_engine(
    'mysql+mysqlconnector://root:' + connection_info.MyPassword + connection_info.MyHost + connection_info.MyDatabase,
    echo=True)
# cnx = mysql.connector.connect(user=connection_info.MyUser, password=connection_info.MyPassword,
#                               host=connection_info.MyHost,
#                               database=connection_info.MyDatabase)
# cursor = cnx.cursor()

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
    moveid = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)

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
    name = sqlalchemy.Column(sqlalchemy.String(length=50), index=True)
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

class StoreAbilityRel(Base):

    __tablename__ = 'abilityrel'

    pokemonid = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    abilityid = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)

    def __init__(self, pokemonid, abilityid):
        self.pokemonid = pokemonid
        self.abilityid = abilityid

    def __repr__(self):
        return "<StoreAbilityRel(pokemonid='{0}', abilityid='{1}'>".format(
            self.pokemonid, self.abilityid)

class StoreAbility(Base):

    __tablename__ = 'ability'

    abilityid = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(length=50), index=True)
    description = sqlalchemy.Column(sqlalchemy.String(length=200))

    def __init__(self, abilityid, name, description):
        self.abilityid = abilityid
        self.name = name
        self.description = description

    def __repr__(self):
        return "<StoreAbility(abilityid='{0}', name='{1}', description='{2}')>".format(
            self.abilityid, self.name, self.description)

class StoreTypeRel(Base):

    __tablename__ = 'typerel'

    pokemonid = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    typeid = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)

    def __init__(self, pokemonid, typeid):
        self.pokemonid = pokemonid
        self.typeid = typeid

    def __repr__(self):
        return "<StoreTypeRel(pokemonid='{0}', typeid='{1}'>".format(
            self.pokemonid, self.typeid)

class StoreType(Base):

    __tablename__ = 'type'

    typeid = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String(length=50))

    def __init__(self, typeid, name):
        self.typeid = typeid
        self.name = name

    def __repr__(self):
        return "<StoreType(abilityid='{0}', name='{1}')>".format(
            self.abilityid, self.name)

class StoreStat(Base):

    __tablename__ = 'statv2'

    pokemonid = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    hp = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    atk = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    defense = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    spatk = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    spdef = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    spd = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)

    def __init__(self, pokemonid, hp, atk, defense, spatk, spdef, spd):
        self.pokemonid = pokemonid
        self.hp = hp
        self.atk = atk
        self.defense = defense
        self.spatk = spatk
        self.spdef = spdef
        self.spd = spd

    def __repr__(self):
        return "<StoreType(pokemonid='{0}', hp='{1}', atk='{2}', defense='{3}', spatk='{4}', spdef='{5}', spd='{6}')>".format(
            self.pokemonid, self.hp, self.atk, self.defense, self.spatk, self.spdef, self.spd)

class AddToTeam(Base):

    __tablename__ = 'team'

    teamid = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    count = sqlalchemy.Column(sqlalchemy.Integer)

    def __init__(self, teamid, count):
        self.teamid = teamid
        self.count = count

    def __repr__(self):
        return "<StoreTeam(teamid='{0}', count='{1}')>".format(
            self.teamid, self.count) 

class AddToTeamRel(Base):

    __tablename__ = 'teamrel'

    pokemonid = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    teamid = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    moveid1 = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    moveid2 = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    moveid3 = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    moveid4 = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)

    def __init__(self, pokemonid, teamid, moveid1, moveid2, moveid3, moveid4):
        self.pokemonid = pokemonid
        self.teamid = teamid
        self.moveid1 = moveid1
        self.moveid2 = moveid2
        self.moveid3 = moveid3
        self.moveid4 = moveid4


    def __repr__(self):
        return "<StoreTeamRel(pokemonid='{0}', teamid='{1}', moveid1='{2}', moveid2='{3}', moveid3='{4}', moveid4='{5}'>".format(
            self.pokemonid, self.teamid, self.moveid1, self.moveid2, self.moveid3, self.moveid4)                  

class AddToComment(Base):

    __tablename__ = 'comment'

    teamid = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    description = sqlalchemy.Column(sqlalchemy.String(length=300))

    def __init__(self, teamid, description):
        self.teamid = teamid
        self.description = description

    def __repr__(self):
        return "<AddToComment(teamid='{0}', description='{1}')>".format(
            self.teamid, self.description)                  

Base.metadata.create_all(engine)  # creates the stores table

# Create a session
Session = sqlalchemy.orm.sessionmaker()
Session.configure(bind=engine)
session = Session()

connection = engine.connect()

# Only run once
# idx_moveid = Index('idx_moveid', StoreMoveRel.moveid)
# idx_movename = Index('idx_movename', StoreMove.name)
# idx_abilityname = Index('idx_abilityname', StoreAbility.name)
#
# idx_moveid.create(bind=engine)
# idx_movename.create(bind=engine)
# idx_abilityname.create(bind=engine)

def getMove(name):
    query = """Select * from move where move.name = %s"""
    arg = (name)
    result_proxy = connection.execute(query, arg)

    results = result_proxy.fetchall()
    if not results:
        return []
    return results[0]
    # try:
    #     cursor.execute(query, arg)
    # except mysql.connector.Error as err:
    #     print(err.msg)
    # for x in cursor:
    #     print(x)

def getAbility(name):
    query = """Select * from ability where ability.name = %s"""
    arg = (name)
    result_proxy = connection.execute(query, arg)

    results = result_proxy.fetchall()
    if not results:
        return []
    return results[0]
