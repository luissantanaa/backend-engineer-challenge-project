import os

from dotenv import load_dotenv
from app.core.database import DatabaseSessionManager


dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.env"))
load_dotenv(dotenv_path=dotenv_path)

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_TEST_DB_NAME = os.getenv("POSTGRES_TEST_DB_NAME")
POSTGRES_SERVER = os.getenv("POSTGRES_SERVER")

SQLALCHEMY_TEST_DATABASE_URL = (
    "postgresql+asyncpg://"
    + POSTGRES_USER
    + ":"
    + POSTGRES_PASSWORD
    + "@"
    + POSTGRES_SERVER
    + "/"
    + POSTGRES_TEST_DB_NAME
)

sessionmanager = DatabaseSessionManager(
    SQLALCHEMY_TEST_DATABASE_URL,
    {"echo": True},
)


async def get_test_db():
    async with sessionmanager.session() as session:
        try:
            yield session
        finally:
            await session.close()
