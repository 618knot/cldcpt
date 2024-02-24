from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
from os.path import join, dirname

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

DB_NAME = os.environ.get("DB_NAME")

engine = create_engine("sqlite:///" + DB_NAME, echo=False)

Base = declarative_base()

maker = sessionmaker(bind=engine)
session = maker()
# session = sessionmaker(bind=engine)