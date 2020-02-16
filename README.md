# GD Level Converter

Converts a level from 2.1 to 1.9 for no reason at all

## Requirements

* Python 3.8
* Requests

## Notes on versions

New releases will only be made if a breaking change is done that will change how levels are parsed. For any other changes, having an updated [objCharts.py](https://raw.githubusercontent.com/zmxhawrhbg/gd-level-converter/master/objCharts.py) should work fine.

## Usage

### Level Converter

`levelConverter.py <id>`  
Converts a level with id `<id>`.  
Will also use the following environment variables as settings:

* `DRY` - don't upload level, use to test if a level will reupload well
* `CLUB` - convert clubstep decoration into lined variants, may fix some decoration while breaking gameplay
* `GLOW` - convert 2.1 glow blocks, may break some decoration

### Level Downloader

`levelDownloader.py <id>`  
Saves a text file named `<level name>.txt`

### Level Util

`levelUtil.py <level file>`  
Converts a level in text named `<level file.txt>` and saves another file named `<level file>-conv.txt`

### Save Util

`saveUtil.py`  
**May be slightly broken**  
**Also requires PyInquirer module**

Put a `CCLocalLevels.dat` in the same directory as `saveUtil.py`.
Does the following actions:

* Exports a level to text file
* Imports a level from text file
