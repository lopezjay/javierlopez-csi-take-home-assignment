# Legal Playlist Generator

## Application for generating Legal Playlists from a collection of Content available in a given Country

## Dependencies
Pydantic (for data model creation and validation)

### Program Structure
legalplaylistgenerator: Library entrypoint where a user will provide a country code and content identifier to generate one or more legal playlists:
```python
l = LegalPlaylistGenerator(inventory_path='inventory.json')
l.generate_playlist("MI3", "CA")
```

```bash
pip3 install -r requirements.txt
python3 legalplaylistgenerator.py
```

```bash
Output:
Playlist1

{V4,V1}

Playlist2

{V6,V3}
```

Note: Pickling is used for serializing objects at rest and reducing overall memory footprint of instantiated objects using byte strings. I recommend using a database or on-disk storage and country or language-based sharding to make this more scalable.

#### Appendix A: Object Definitions
* Content: A licensed asset used as a logical abstraction for a movie or a TV show episode. It is directly associated with 0 or more ordered Pre-Rolls.

* Pre-Roll: A licensed asset used as a logical abstraction for Video clips that play before an associated piece of Content. It is directly associated with 0 or more pieces of Content. The associated Pre-Rolls for a given piece of Content will play in a definite sequence prior to the Content.

* Video: A digital video file associated with a piece of Content or a Pre-Roll. Each piece of Content or Pre-Roll may have 1 or more associated Videos. Each Video is uniquely tagged with a single Language and a list of available Countries where it may air.

* Playlist: An ordered legal sequence of Pre-Rolls and pieces of Content given as input instructions to a Media Player. All Videos associated with the pieces of Content and Pre-Rolls in a Playlist will have matching Country and Language attributes in order to form a legal play sequence.