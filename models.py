# importing Base that will allow us to create each of our database models or classes (ORM models)
from .database import Base

# Importing sqlalchemy datatypes to be used and relationship for relevant tables
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

# Creating classes that inherit from the imported Base class that are SQLAlchemy models
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="item_owner")
    blogs = relationship("Blog", back_populates="blog_owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    item_owner = relationship("User", back_populates="items")


class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String, index=True)
    created_on = Column(DateTime, index=True)
    post_owner_id = Column(Integer, ForeignKey("users.id"))

    blog_owner = relationship("User", back_populates="blogs")


