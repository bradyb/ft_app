from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
 
engine = create_engine('sqlite:///testfrench2017.db', echo=True)
Base = declarative_base()
 
########################################################################
class players(Base):
    """"""
    __tablename__ = "players"
 
    name = Column(String, primary_key=True)
    date = Column(String, primary_key=True)
    aces = Column(Integer)
    double_faults  = Column(Integer)
    winners = Column(Integer)
    unforced_errors = Column(Integer)
    second_srv_percent = Column(Integer)
    receive_percent = Column(Integer)
    bps  = Column(Integer)
    bpl  = Column(Integer)
    bpc  = Column(Integer)

    #----------------------------------------------------------------------
    def __init__(self, name, date, aces, double_faults, 
                        winners, unforced_errors, second_srv_percent, receive_percent, bps, bpc, bpl):
        """"""
        self.name = name
        self.date = date
        self.aces = aces
        self.double_faults = double_faults
        self.winners = winners
        self.unforced_errors = unforced_errors
        self.second_srv_percent = second_srv_percent
        self.receive_percent = receive_percent
        self.bps = bps
        self.bpc = bpc
        self.bpl = bpl

class User(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True)
    password = Column(String)
    totalPoints = Column(Integer)

#----------------------------------------------------------------------
    def __init__(self, username, password):
        """"""
        self.username = username
        self.password = password
        self.totalPoints = 0


class Teams(Base):
    __tablename__ = "teams"

    username = Column(String, primary_key=True)
    player_name = Column(String, primary_key=True)
    attribute = Column(Integer)
    benched = Column(Integer)
    alive = Column(Integer)

    def __init__(self, username, player_name, attribute, benched):

        self.username = username
        self.player_name = player_name
        self.attribute = attribute
        self.benched = benched
        self.alive = 1

 
# create tables
Base.metadata.create_all(engine)