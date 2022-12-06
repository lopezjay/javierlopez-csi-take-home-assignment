"""
contentprerollpair.py

Object Model Definition for Content Preroll Pair
"""

# Standard Library Imports

# Third Party Imports
from pydantic import BaseModel, validator

# Local Imports

class ContentPrerollPair(BaseModel):
    """
    SQL Table Defintion
    -------------------
    content varchat(255) NOT NULL,
    playorder int NOT NULL,
    preroll varchar(255) NOT NULL,
    FOREIGN KEY (content) REFERENCES Content(name)
    FOREIGN KEY (preroll) REFERENCES Preroll(name)
    """
    content: str
    preroll: str
    playorder: int

    @validator('content')
    def content_must_not_be_empty(cls, value):
        if not len(value):
            raise ValueError("Content cannot be empty")
        return value

    @validator('preroll')
    def preroll_must_not_be_empty(cls, value):
        if not len(value):
            raise ValueError("Preroll cannot be empty")
        return value

    @validator('playorder')
    def playorder_must_be_positive_valued(cls, value):
        if len(value) < 1:
            raise ValueError("Play Order must be a positive integer")
        return value