"""
content.py

Object Model Definition for Content
"""

# Standard Library Imports
from typing import List

# Third Party Imports
from pydantic import BaseModel, validator

# Local Imports
from models.video import Video


class ContentPreroll(BaseModel):
    """
    Helper Object Model for Pre-Rolls associated
    with a piece of Content

    name: str
        Name associated with a piece of Content
    """

    name: str

    @validator('name')
    def name_must_not_be_empty(cls, value):
        if not value:
            raise ValueError("Name cannot be empty")
        return value


class Content(BaseModel):
    """
    Object Model for a piece of Content

    Attributes
    ----------
    name: str
        Name associated with a piece of Content
    preroll: List[ContentPreroll]
        An ordered sequence of Pre-Rolls 
        associated with a piece of Content
    videos: List[Video]
        An unordered sequence of Videos
        associated with a piece of Content
    """

    name: str
    preroll: List[ContentPreroll]
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