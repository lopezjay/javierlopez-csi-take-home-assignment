"""
countrycontentpair.py

Object Model Definition for Content-Country pairs
"""

# Standard Library Imports

# Third Party Imports
from pydantic import BaseModel, validator

# Local Imports
from content import Content
from country import Country


class CountryContentPair(BaseModel):
    """
    SQL Table Defintion
    -------------------
    content varchar(255) NOT NULL,
    country varchar(255) NOT NULL,
    """
    content: str
    country: str

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