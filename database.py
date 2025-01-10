from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = "Enter your database URL here"
engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

SessionDep = Annotated[Session, Depends(get_session)]

