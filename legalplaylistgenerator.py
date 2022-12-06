"""
legalplaylistgenerator.py

Legal Playlist Generator Library
"""

# Standard Library Imports
import json
import pickle

# Local imports
from models.content import Content
from models.preroll import Preroll
from models.video import Video

class AssetInventory:
    # Declare logical asset types
    logical_assets = {
        "content": Content,
        "preroll": Preroll,
    }

    # Declare physical asset types
    physical_assets = {
        "video": Video
    }

    def __init__(self):
        pass

    def create_asset_tables(self, asset_category: str):
        asset_types = getattr(self, f"{asset_category}_assets", None)

        if not asset_types:
            raise ValueError("f{asset_category} is not a known asset category")

        for asset_type in asset_types:
            asset_table = getattr(self, f"{asset_type}_table", None)

            if not asset_table:
                setattr(self, f"{asset_type}_table", {})

    def create_logical_asset_tables(self):
        self.create_asset_tables("logical")

    def create_physical_asset_tables(self):
        self.create_asset_tables("physical")

    def load_inventory(self, inventory):
        self.create_logical_asset_tables()

        self.create_physical_asset_tables()

        for asset_type in inventory:
            if not asset_type in self.logical_assets:
                continue

            asset_list = inventory[asset_type]

            for asset_item in asset_list:
                asset = self.logical_assets[asset_type].parse_obj(asset_item)

                asset_table = getattr(self, f"{asset_type}_table", None)

                asset_table[asset.name] = pickle.dumps(asset)


# Parse input inventory
with open("inventory.json") as inventory_file:
    inventory = json.load(inventory_file)

a = AssetInventory()

a.load_inventory(inventory)

print(pickle.loads(a.content_table["MI3"]))
print(pickle.loads(a.preroll_table["WB1"]))

# class LegalPlaylistGenerator: