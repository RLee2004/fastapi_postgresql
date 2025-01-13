from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = "postgresql://USER:PASSWORD@localhost:5432/DBNAME"
engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

SessionDep = Annotated[Session, Depends(get_session)]

