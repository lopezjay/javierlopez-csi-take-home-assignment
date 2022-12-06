"""
preroll.py

Object Model Definition for Pre-Rolls
"""

# Standard Library Imports
from typing import List

# Third Party Imports
from pydantic import BaseModel, validator

# Local imports
from models.video import Video


class Preroll(BaseModel):
    """
    Object Model for a Pre-Roll

    Attributes
    ----------
    name: str
        Name associated with a Pre-Roll
    videos: List[Video]
        An unordered sequence of Videos
        associated with a Pre-Roll
    """

    name: str
    videos: List[Video]

    @validator('name')
    def name_must_not_be_empty(cls, value):
        if not value:
            raise ValueError("Name cannot be empty")
        return value

    @validator('videos')
    def videos_must_not_be_empty(cls, value):
        if not value:
            raise ValueError("Videos cannot be empty")
        return value