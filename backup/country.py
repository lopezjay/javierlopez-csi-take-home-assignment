"""
country.py

Object Model Definition for Countries
"""

# Standard Library Imports

# Third Party Imports
from pydantic import BaseModel, validator


class Country(BaseModel):
    """
    name varchar(255) NOT NULL,
    PRIMARY KEY (name)
    """
    name: str

    @validator('name')
    def name_must_not_be_empty(cls, value):
        if not len(value):
            raise ValueError("Name cannot be empty")
        return value