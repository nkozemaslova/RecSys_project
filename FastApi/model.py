from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, Text
from database import Base
import enum

class Users(Base):
    __tablename__ = "Users"
    USER_ID = Column(Integer,primary_key=True,index=True)
    UserName = Column(String(255))

class Artists(Base):
    __tablename__ = "Artists"
    ARTIST_ID = Column(Integer,primary_key=True,index=True)
    ArtistName = Column(String(255))
    GANRE_ID = Column(Integer,index=True)

class Ganres(Base):
    __tablename__ = "Ganres"
    GANRE_ID = Column(Integer,primary_key=True,index=True)
    GanreName = Column(String(255))

class Songs(Base):
    __tablename__ = "Songs"
    SONG_ID = Column(Integer,primary_key=True,index=True)
    Title = Column(String(255))
    ARTIST_ID = Column(Integer,index=True)
    GANRE_ID = Column(Integer,index=True)

class Interactions(Base):
    __tablename__ = "Interactions"
    INTERACTION_ID = Column(Integer,primary_key=True,index=True)
    USER_ID = Column(Integer)
    SONG_ID = Column(Integer)
    Score = Column(Integer)