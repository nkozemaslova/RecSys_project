from sqlalchemy.schema import Column
from sqlalchemy.types import String, Integer, Text
from database import Base
import enum

class User(Base):
    __tablename__ = "Users"
    id = Column(Integer)
    name = Column(String(30))
