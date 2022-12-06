"""
video.py

Object Model Definition for Videos
"""

# Standard Library Imports
from typing import List, Optional

# Third Party Imports
from pydantic import BaseModel, validator


class VideoAttributes(BaseModel):
    """Helper Object Model for Video Attributes
    
    Attributes
    ----------
    countries: List[str]
        Countries associated with a Video
    language: str
        Language associated with a Video
    """

    countries: List[str]
    language: str

    @validator('countries')
    def countries_must_not_be_null(cls, value):
        if not value:
            raise ValueError("Countries cannot be empty")
        return value

    @validator('countries', each_item=True)
    def countries_each_item_must_not_be_null(cls, value):
        if not value:
            raise ValueError("Country cannot be empty")
        return value

    @validator('language')
    def language_must_not_be_null(cls, value):
        if not value:
            raise ValueError("Language cannot be empty")
        return value


class PlaylistVideo(BaseModel):
    """
    Object Model for a unique Video belonging to a playlist

    Attributes
    ----------
    name: str
        Name associated with a Video
    content: Optional[str]
        Piece of Content that a Video is attached to (if available)
    country: str
        Country associated with a Video
    language: str
        Language associated with a Video
    preroll: Optional[str]
        Pre-Roll that a Video is attached to (if available)
    """

    name: str
    content: Optional[str]
    country: str
    language: str
    preroll: Optional[str]

    @validator('name')
    def name_must_not_be_null(cls, value):
        if not value:
            raise ValueError("Name cannot be empty")
        return value

    @validator('country')
    def country_must_not_be_null(cls, value):
        if not value:
            raise ValueError("Country cannot be empty")
        return value

    @validator('language')
    def language_must_not_be_null(cls, value):
        if not value:
            raise ValueError("Language cannot be empty")
        return value


class Video(BaseModel):
    """
    Object Model for a Video

    Attributes
    ----------
    name: str
        Name associated with a Video
    attributes: VideoAttributes
        Attributes associated with a Video
    """

    name: str
    attributes: VideoAttributes

    @validator('name')
    def name_must_not_be_null(cls, value):
        if not value:
            raise ValueError("Name cannot be empty")
        return value

    @validator('attributes')
    def attributes_must_not_be_null(cls, value):
        if not value:
            raise ValueError("Attributes cannot be null")
        return value

    @classmethod
    def to_playlist_video(cls, video_asset: BaseModel, parent_asset: BaseModel) -> List[PlaylistVideo]:
        parent_asset_type = type(parent_asset).__name__.lower()

        for country in video_asset.attributes.countries:
            result_obj = PlaylistVideo(name=video_asset.name, country=country, language=video_asset.attributes.language)

            setattr(result_obj, parent_asset_type, parent_asset.name)

            yield result_obj