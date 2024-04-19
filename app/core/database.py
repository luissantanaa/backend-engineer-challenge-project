import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.env"))
load_dotenv(dotenv_path=dotenv_path)

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB_NAME = os.getenv("POSTGRES_DB_NAME")
POSTGRES_SERVER = os.getenv("POSTGRES_SERVER")

SQLALCHEMY_DATABASE_URL = (
    "postgresql://"
    + POSTGRES_USER
    + ":"
    + POSTGRES_PASSWORD
    + "@"
    + POSTGRES_SERVER
    + "/"
    + POSTGRES_DB_NAME
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
