from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

DATABASE_URL = "mysql+mysqldb://zaderu:zaderu@localhost:3306/project"
#"root:1234@tcp(localhost:3306)/golang?charset=utf8"


db_engine = create_engine(DATABASE_URL)

connection = db_engine.connect()

factory = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
session = factory()

