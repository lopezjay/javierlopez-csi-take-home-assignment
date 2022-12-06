"""
legalplaylistgenerator.py

Legal Playlist Generator Library
"""

# Standard Library Imports
import json
import pickle
from typing import List

# Third Party Imports
from pydantic import BaseModel

# Local imports
from models.content import Content
from models.preroll import Preroll
from models.video import Video


class AssetTableGenerator:
    """
    Class for handling asset inventory data
    and populating asset tables for optimized lookup
    """
    # Declare logical asset types
    logical_assets = {
        "content": Content,
        "preroll": Preroll,
    }

    # Declare physical asset types
    physical_assets = {
        "video": Video
    }

    def create_asset_table(self, asset_type: str) -> None:
        """
        Create an Asset table for optimized lookup
        """

        asset_table = getattr(self, f"{asset_type}_table", None)

        if not asset_table:
            setattr(self, f"{asset_type}_table", {})

    def create_asset_tables_by_category(self, asset_category: str) -> None:
        """
        Create Asset tables for a given Asset category
        """

        asset_types = getattr(self, f"{asset_category}_assets", None)

        if not asset_types:
            raise ValueError("f{asset_category} is not a known asset category")

        for asset_type in asset_types:
            self.create_asset_table(asset_type)

    def create_logical_asset_tables(self) -> None:
        """Create Asset tables for Logical assets"""
        self.create_asset_tables_by_category("logical")

    def create_physical_asset_tables(self) -> None:
        """Create Asset tables for Physical assets"""
        self.create_asset_tables_by_category("physical")

    def get_asset_table(self, asset_type: str) -> dict:
        return getattr(self, f"{asset_type}_table", None)

    def get_all_assets_from_table(self, asset_type: str) -> List[BaseModel]:
        asset_table = self.get_asset_table(asset_type)

        if asset_table:
            return [asset_table[asset_name] for asset_name in asset_table]

    def get_asset_from_table(self, asset_type: str, asset_name: str) -> BaseModel:
        asset_table = self.get_asset_table(asset_type)

        if asset_table:
            return asset_table.get(asset_name)

    def update_asset_table(self, asset_type: str, asset: BaseModel, asset_key: str=None) -> None:
        asset_table = self.get_asset_table(asset_type)

        if asset_table is not None:
            asset_table[asset_key or asset.name] = pickle.dumps(asset)

    def run(self, inventory: dict) -> None:

        # Initialize Asset tables
        self.create_logical_asset_tables()

        self.create_physical_asset_tables()

        # Get top level Logical assets from the inventory
        for logical_asset_type in inventory:
            if not logical_asset_type in self.logical_assets:
                continue

            asset_list = inventory[logical_asset_type]

            for logical_asset_data in asset_list:
                logical_asset = self.logical_assets[logical_asset_type].parse_obj(logical_asset_data)

                for video in logical_asset.videos:
                    for playlist_video in Video.to_playlist_video(video, logical_asset):

                        playlist_video_key = f"{playlist_video.name}_{playlist_video.country}_{playlist_video.language}"

                        self.update_asset_table("video", playlist_video, playlist_video_key)

                self.update_asset_table(logical_asset_type, logical_asset)


class LegalPlaylistGenerator:
    def __init__(self) -> None:
        self.playlist = []
        self.assets = []

    def generate_playlist(self, content_name: str, country: str):
        pass


# Parse input inventory
with open("inventory.json") as inventory_file:
    inventory = json.load(inventory_file)

a = AssetTableGenerator()

a.run(inventory)

print(pickle.loads(a.get_asset_table("content")["MI3"]))
print(pickle.loads(a.get_asset_table("preroll")["WB1"]))
for k,v in a.get_asset_table("video").items():
    print(pickle.loads(v))
