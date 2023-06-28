from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine

# * This is the database URL that will be used to connect to the database and create the tables

# TODO: Just uncomment your Database url and comment the other one
# TODO : Thanks Bro <3

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:manga2023@localhost/db1"

# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:mypassword@localhost/GP-Database"

# * Create the engine that will be used to connect to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# * Create the base that will be used to create the tables in the database
Base = declarative_base()

# * Create the session that will be used to create the tables
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


# * Create a function that will be used to get the database session and close it after the request is done
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
