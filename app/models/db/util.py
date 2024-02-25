from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
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

engine = create_engine("sqlite:///" + DB_NAME, echo=False)
# engine = create_engine(f"mysql+pymysql://{USER_NAME}:{PASSWORD}@{DB_HOST}:3306/{DB_NAME}?utf8mb4", echo=False)

Base = declarative_base()

maker = sessionmaker(bind=engine)
session = maker()