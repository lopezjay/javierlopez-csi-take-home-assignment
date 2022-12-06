"""
playlistvideopair.py

Object Model Definition for Playlist Video Pair
"""

# Standard Library Imports

# Third Party Imports
from pydantic import BaseModel, validator

# Local Imports
from content import Content
from country import Country
from language import Language
from video import Video


class PlaylistVideoPair(BaseModel):
    """
    SQL Table Defintion
    -------------------
    content varchat(255) NOT NULL,
    country varchar(255) NOT NULL,
    language varchar(255) NOT NULL,
    playorder int NOT NULL,
    video varchar(255) NOT NULL,
    FOREIGN KEY (content) REFERENCES Content(name)
    FOREIGN KEY (country) REFERENCES Country(name)
    FOREIGN KEY (language) REFERENCES Language(name)
    FOREIGN KEY (video) REFERENCES Videos(name)
    """

    content: Content
    country: Country
    language: Language
    playorder: int
    video: Video

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

    @validator('playorder')
    def playorder_must_be_positive_valued(cls, value):
        if len(value) < 1:
            raise ValueError("Play Order must be a positive integer")
        return value

    @validator('video')
    def content_must_not_be_empty(cls, value):
        if not len(value):
            raise ValueError("Video cannot be empty")
        return value