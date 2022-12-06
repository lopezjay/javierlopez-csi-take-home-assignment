"""
legalplaylistgenerator.py

Legal Playlist Generator Library
"""

# Standard Library Imports
import json
import pickle

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

    def _create_asset_table(self, asset_type: str) -> None:
        """
        Create an Asset table for optimized lookup
        """

        asset_table = getattr(self, f"{asset_type}_table", None)

        if not asset_table:
            setattr(self, f"{asset_type}_table", {})

    def _create_asset_tables_by_category(self, asset_category: str) -> None:
        """
        Create Asset tables for a given Asset category
        """

        asset_types = getattr(self, f"{asset_category}_assets", None)

        if not asset_types:
            raise ValueError("f{asset_category} is not a known asset category")

        for asset_type in asset_types:
            self._create_asset_table(asset_type)

    def get_asset_table(self, asset_type: str) -> dict:
        return getattr(self, f"{asset_type}_table", None)

    def get_asset_from_table(self, asset_type: str, asset_name: str) -> BaseModel:
        asset_table = self.get_asset_table(asset_type)

        if asset_table:
            asset = asset_table.get(asset_name)
            return pickle.loads(asset) if asset else None

    def update_asset_table(self, asset_type: str, asset: BaseModel, asset_key: str=None) -> None:
        asset_table = self.get_asset_table(asset_type)

        if asset_table is not None:
            asset_table[asset_key or asset.name] = pickle.dumps(asset)

    def generate_asset_tables(self, inventory: dict) -> None:

        # Initialize Asset tables
        self._create_asset_tables_by_category("logical")
        self._create_asset_tables_by_category("physical")

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
    def __init__(self, inventory_path: str="inventory.json") -> None:
        self.inventory_path = inventory_path
        self._playlists = {}
        self._asset_table_generator = None

    def _generate_assets(self) -> None:
        # Parse input inventory file
        inventory = {}

        try:
            with open(self.inventory_path, "r") as inventory_file:
                inventory = json.load(inventory_file)
        except Exception as err:
            print(f"Could not parse inventory file {self.inventory_path}: {repr(err)}")
        else:
            self._asset_table_generator = AssetTableGenerator()
            self._asset_table_generator.generate_asset_tables(inventory)

    def generate_playlist(self, content_name: str, country: str):
        self._generate_assets()

        content = self._asset_table_generator.get_asset_from_table("content", content_name)

        video_asset_table = self._asset_table_generator.get_asset_table("video")

        if not content:
            print(f"Content not found: {content_name}")
            return

        if content.preroll:
            for content_preroll in content.preroll:
                preroll = self._asset_table_generator.get_asset_from_table("preroll", content_preroll.name)

                if not preroll:
                    print(f"Pre-Roll not found: {content_preroll.name}")
                    continue

            for video_key in video_asset_table:
                video = self._asset_table_generator.get_asset_from_table("video", video_key)

                if video.country == country and video.preroll == preroll.name:
                    if video.language not in self._playlists:
                        self._playlists[video.language] = []
    
                    if video not in self._playlists[video.language]:
                        self._playlists[video.language].append(video)
    
        for video_key in video_asset_table:
            video = self._asset_table_generator.get_asset_from_table("video", video_key)

            if video.country == country and video.content == content_name:
                if video.language not in self._playlists:
                    self._playlists[video.language] = []

                if video not in self._playlists[video.language]:
                    self._playlists[video.language].append(video)

        for language in list(self._playlists.keys()):
            if len(self._playlists[language]) <= 1:
                del self._playlists[language]

        if not self._playlists:
            print("No legal playlist(s) possible")
            return

        playlist_ctr = 1
        for playlist in self._playlists.values():
            playlist_str = "{" + ','.join([video.name for video in playlist]) + "}"
            print(f"Playlist{playlist_ctr}\n\n{playlist_str}\n")
            playlist_ctr += 1


l = LegalPlaylistGenerator(inventory_path="inventory.json")
l.generate_playlist("MI3", "US")