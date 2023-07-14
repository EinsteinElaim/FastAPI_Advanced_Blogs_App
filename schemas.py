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


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


# Pydantic models for the Blog database model
class BlogBase(BaseModel):
    title: str
    content: str
    created_on: datetime


class BlogCreate(BlogBase):
    pass


class Blog(BlogBase):
    id: int
    post_owner_id: int

    class Config:
        orm_mode = True


# Pydantic models for the User database model
class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []
    blogs: list[Blog] = []

    class Config:
        orm_mode = True
