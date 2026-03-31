from sqlalchemy import create_engine #creating the database engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

#others
import os

#type safety
from typing import Annotated
from fastapi import Depends



#Database URL for local sql
BASE_SQL_URL = "sqlite:///./records.db"


#Database connection engine
engine = create_engine(
    BASE_SQL_URL,
    connect_args={"check_same_thread": False}
)




#Databse Session for the Application
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


#Database base
Base = declarative_base()


#Function to help quickly talks to our database

def get_db():
    db = SessionLocal()

    #try to open the database
    try:
        yield db
    finally:
        db.close()

    

#Annoted to combine and connect our Session and Base
DbSession = Annotated[Session, Depends(get_db)]








