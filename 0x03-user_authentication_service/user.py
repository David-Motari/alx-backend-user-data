#!/usr/bin/env python3
"""
user model
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    model for user in 'users' table
    """

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
