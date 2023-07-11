# Adding imports for sqlalchemy parts needed
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# creating a database URL for sqlalchemy
SQLALCHEMY_DATABASE_URL = "sqlite:///./fast_api_advanced_tutorial.db"
# for postgresql
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"


# Creating the SQLAlchemy engine and setting False the check_same_thread argument to allow more than one thread access
# the database for the same request
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# creating a SessionLocal class which each instance of it is a database session.
# So, the once we create an instance of the SessionLocal class,
# that will be the actual database session and not the class itself
# we name it SessionLocal to distinguish it from the Session we are importing from SQLAlchemy which we will use later
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Creating a 'Base' class using declarative_base() function that returns a class
# Later, we will inherit from this Base class to create each of our database models or classes (the ORM models)
Base = declarative_base()

