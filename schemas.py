# This file only contains the Pydantic models and not the SQLAlchemy models that are only contained in the models file
# This file/the Pydantic models define more or less a "schema" (a valid data shape)

# Creating initial Pydantic models/schemas for our database models that are 'ItemBase', 'BlogBase' and 'UserBase'
# They should have common attributes while creating or reading data
# Also, create 'ItemCreate', 'BlogCreate' and 'UserCreate' Pydantic models that inherit from the respective Base models
# The user will have a 'password' when creating it, but for security,
# but the 'password' won't be in any other Pydantic models, for example:
# It won't be sent from the API when reading a user

# Importing Pydantic BaseModel do define our models for Pydantic schema
from pydantic import BaseModel
from datetime import *


# Pydantic models for the Item database model
class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


# This is the Pydantic model for reading Item class instances that give us from the API,
# an ID and OWNER_ID for Item instances
class Item(ItemBase):

    id: int
    owner_id: int

    # In this Pydantic class for reading,
    # we add an internal Config class that's used to provide configuration to Pydantic.
    # In the Config class, we set the attribute 'orm_mode = True'
    # It does not use a : as for the Type declaration since this is a config value, not declaring a type
    # Pydantic's 'orm_mode' will tell the Pydantic model to read the data even if it's not a 'dict',
    # but an ORM model(or any other arbitrary object with attributes)
    # This is why, instead of trying to get only the 'id' value from a 'dict', as in 'id = dat["id"]',
    # it will also try to get it from an attribute, as in: 'id = data.id'.

    # With this, the Pydantic model is compatible with ORM's and
    # one can declare it in the 'response_model' argument in one's *path operations*
    # And one will be able to return a database model and it will read the data from it.
    # Bypasses lazy loading for SQLAlchemy
    class Config:
        orm_mode = True


# Pydantic models for the Blog database model
class BlogBase(BaseModel):
    title: str
    content: str
    created_on: datetime


class BlogCreate(BlogBase):
    pass


# This is the Pydantic model for reading Blog class instances that give us from the API,
# an ID and OWNER_ID for Blog instances
class Blog(BlogBase):
    id: int
    post_owner_id: int

    # In this Pydantic class for reading,
    # we add an internal Config class that's used to provide configuration to Pydantic.
    # In the Config class, we set the attribute 'orm_mode = True'
    # It does not use a : as for the Type declaration since this is a config value, not declaring a type
    # Pydantic's 'orm_mode' will tell the Pydantic model to read the data even if it's not a 'dict',
    # but an ORM model(or any other arbitrary object with attributes)
    # This is why, instead of trying to get only the 'id' value from a 'dict', as in 'id = dat["id"]',
    # it will also try to get it from an attribute, as in: 'id = data.id'.

    # With this, the Pydantic model is compatible with ORM's and
    # one can declare it in the 'response_model' argument in one's *path operations*
    # And one will be able to return a database model and it will read the data from it.
    # Bypasses lazy loading for SQLAlchemy
    class Config:
        orm_mode = True


# Pydantic models for the User database model
class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


# This is the Pydantic model for reading User class instances that give us from the API,
# an ID, IS_ACTIVE, ITEMS list for each ID and BLOGS list for each ID for Item instances
# We use the id fields shared/read from the api in Item and Blog to find the specific instances from these lists here
class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []
    blogs: list[Blog] = []

    # In this Pydantic class for reading,
    # we add an internal Config class that's used to provide configuration to Pydantic.
    # In the Config class, we set the attribute 'orm_mode = True'
    # It does not use a : as for the Type declaration since this is a config value, not declaring a type
    # Pydantic's 'orm_mode' will tell the Pydantic model to read the data even if it's not a 'dict',
    # but an ORM model(or any other arbitrary object with attributes)
    # This is why, instead of trying to get only the 'id' value from a 'dict', as in 'id = dat["id"]',
    # it will also try to get it from an attribute, as in: 'id = data.id'.

    # With this, the Pydantic model is compatible with ORM's and
    # one can declare it in the 'response_model' argument in one's *path operations*
    # And one will be able to return a database model and it will read the data from it.
    # Bypasses lazy loading for SQLAlchemy
    class Config:
        orm_mode = True
