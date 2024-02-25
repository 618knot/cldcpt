from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
from os.path import join, dirname

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

USER_NAME = os.environ.get("USER_NAME")
PASSWORD = os.environ.get("PASSWORD")
DB_NAME = os.environ.get("DB_NAME")
DB_HOST = os.environ.get("DB_HOST")
print(DB_NAME)

engine = create_engine(f"sqlite:///{DB_NAME}", echo=True)
# engine = create_engine(f"mysql+pymysql://{USER_NAME}:{PASSWORD}@{DB_HOST}:3306/{DB_NAME}?utf8mb4", echo=False)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    session = Column(String)

Base.metadata.create_all(bind=engine)