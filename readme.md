# Legal Playlist Generator

## Application for generating Legal Playlists from a collection of Content available in a given Country

### Program Structure
app.py: Application entry point provided as a CLI where 

###


#### Appendix A: Object Definitions
* Content: A licensed asset used as a logical abstraction for a movie or a TV show episode. It is directly associated with 0 or more ordered Pre-Rolls.

* Pre-Roll: A licensed asset used as a logical abstraction for Video clips that play before an associated piece of Content. It is directly associated with 0 or more pieces of Content. The associated Pre-Rolls for a given piece of Content will play in a definite sequence prior to the Content.

* Video: A digital video file associated with a piece of Content or a Pre-Roll. Each piece of Content or Pre-Roll may have 1 or more associated Videos. Each Video is uniquely tagged with a single Language and a list of available Countries where it may air.

* Playlist: An ordered legal sequence of Pre-Rolls and pieces of Content given as input instructions to a Media Player. All Videos associated with the pieces of Content and Pre-Rolls in a Playlist will have matching Country and Language attributes in order to form a legal play sequence.