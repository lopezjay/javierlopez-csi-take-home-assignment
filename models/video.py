"""
video.py

Object Model Definition for Videos
"""

# Standard Library Imports

# Third Party Imports
from pydantic import BaseModel, validator


class Video(BaseModel):
    """
    name varchar(255) NOT NULL,
    content varchar(255),
    country varchar(255) NOT NULL,
    language varchar(255) NOT NULL,
    preroll varchar(255),
    PRIMARY KEY (name)
    """
    name: str
    content: str
    country: str
    language: str
    preroll: str

    @validator('name')
    def name_must_not_be_empty(cls, value):
        if not len(value):
            raise ValueError("Name cannot be empty")
        return value

    @validator('content')
    def content_must_not_be_empty(cls, value):
        if not len(value):
            raise ValueError("Content cannot be empty")
        return value

    @validator('country')
    def country_must_not_be_empty(cls, value):
        if not len(value):
            raise ValueError("Country cannot be empty")
        return value

    @validator('language')
    def language_must_not_be_empty(cls, value):
        if not len(value):
            raise ValueError("Language cannot be empty")
        return value

    @validator('preroll')
    def preroll_must_not_be_empty(cls, value):
        if not len(value):
            raise ValueError("Preroll cannot be empty")
        return value