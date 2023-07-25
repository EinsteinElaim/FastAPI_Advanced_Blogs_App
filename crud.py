# Importing Session to allow us declare the type of 'db' parameters and have better type checks and
# completion in our functions
from sqlalchemy.orm import Session

# Importing the 'models' (SQLAlchemy models) and 'schemas' (Pydantic models)
from . import models, schemas


# CRUD
# Create utility function to:

# Reading utility functions only retrieve records from the database and each request has to have a
# Session parameter passed to it to ensure each read function is its own unique database session

# READING functions only utilises the DATABASE MODELS 'models/SQLAlchemy models' to fetch data from database

# Read a single user by ID
def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


# Read a single user by EMAIL
def get_user_by_email(db: Session, user_email: str):
    return db.query(models.User).filter(models.User.email == user_email).first()


# Read multiple users
def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


# Read a single Item by ID
def get_item_by_id(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()


# Read multiple items
def get_all_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


# Read a single blog by ID
def get_blog_by_id(db: Session, blog_id: int):
    return db.query(models.Blog).filter(models.Blog.id == blog_id).first()


# Read multiple blog posts
def get_all_blogs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Blog).offset(skip).limit(limit).all()


# Creating utility functions to:

# CREATE DATA

# These utility functions will make use of our 'Pydantic models/schemas'
# and also requires their own Session since they are a separate request

# Create a User:
# A user creation utility function needs a Session of it's own to access the db,
# and also needs to access the User's Pydantic model/schema for creation guideline that is UserCreate class
def create_user(db: Session, user: schemas.UserCreate):
    # This is where we configure the temporary but mandatory password field/pre-process it
    # for the actual db record od a user
    fake_hashed_password = user.password + "notreallyhashed"
    #
    # We first create the SQLAlchemy model instance with our user data
    # We also load the now processed password field and assign it's result to the hashed_password field
    # that actually makes it to the database/user account
    #
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    # we add the instance object to our database session
    #
    # The models/SQLAlchemy database models is the one actually responsible to create or transact database operations
    # The schemas/Pydantic models only guides the data input and output
    #
    db.add(db_user)
    # Committing the changes to the database (so as to save the user record)
    db.commit()
    #
    # Refreshing our created instance 'db_user' so it contains any new data from the database,
    # like the generated id and is_active
    #
    db.refresh(db_user)
    # returning our finalised user instance/account created
    return db_user


# Create a user Item:
def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    #
    # Instead of passing each of the keyword arguments to 'Item' and reading each one of them from the Pydantic *model*,
    # we are generating a 'dict/model_dump' with the Pydantic *model*'s data using 'item.model_dump()
    #
    # Then we are passing the 'dict/model_dump' 's key-value pairs as the keyword arguments
    # to the SQLAlchemy 'Item' with:
    # 'Item(**item.model_dump())'
    #
    # We then pass the extra keyword argument 'owner_id' that is not provided by the Pydantic *model* with:
    # 'Item(**item.model_dump(), owner_id=user_id)'
    #
    # We use **item.model_dump instead of .dict since .dic is deprecated
    # db_item = models.Item(**item.dict(), owner_id=user_id)
    #
    db_item = models.Item(**item.model_dump(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# Creating a User Blog:
def create_user_blog(db: Session, blog: schemas.BlogCreate, owner_id: int):
    db_blog = models.Blog(**blog.model_dump(), post_owner_id=owner_id)
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog
