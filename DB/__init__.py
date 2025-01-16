from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Creating engine
engine = create_engine("sqlite:///event_management.db")

# Creating Session
session = sessionmaker(autoflush=False, autocommit=False, bind=engine)

# Base model
Base = declarative_base()
