import os

import sqlmodel
from sqlmodel import Session, SQLModel

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise NotImplementedError("`DATABASE_URL` is not set")

DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg://")

engine = sqlmodel.create_engine(DATABASE_URL)

# database models
def init_db():
    print("Initializing database / Creating database tables...")
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session