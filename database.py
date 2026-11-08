import os

from dotenv import load_dotenv

from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker

from models import Base


load_dotenv()

DATABASE_URL = URL.create(
    "postgresql+psycopg2",
    username=os.environ["DB_USERNAME"],
    password=os.environ["DB_PASSWORD"],
    host=os.environ["DB_HOST"],
    port=os.environ["DB_PORT"],
    database=os.environ["DB_NAME"]
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


def init_db():
    Base.metadata.create_all(bind=engine)