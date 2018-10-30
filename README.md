# Adobe-XMP-Tools

Adobe-XMP-Tools is a library dedicated to parsing Adobe XMP files into .csv for training in Keras.

## Getting Started
---
#### Parsing
Parser will take 2 folder paths to instantiate
- where you wish to save the JPEGS
- where you wish to save the parsed CSV data

```python
from brycetools.parsing import Parser
myParser = Parser(r"C:/Jpeg/dir/path": str, r"C"/Data/dir/path": str)

# camera types only support "Canon or Sony"
# more raw file types can be added by altering set_camera_type to include file extenions of any brand
myParser.set_camera_type("canon" or "sony")

# add a folder containing (XMP's & RAW files) or just XMP files to the folders list
# this list will contain the folders containing data to be parsed
myParser.addFolder(r"C:/folder/containing/": str)
# or to add a list of folders
listOfFolders = [list of folder paths]
myParser.addFolders(listOfFolders: list)

# parse the data
myParser.parse()
# save parsed data to the data dir
myParser.save()
# or, parse into a variable and save from there
myData = myParser.parse()
```
