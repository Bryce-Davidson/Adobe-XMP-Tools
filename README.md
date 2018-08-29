# brycetools
#### brycetools is a library built for preparing Adobe XMP data for training in keras
---
### Parsing XMP files into Pandas DataFrame
```python
from brycetools.parsing import Parser

# creating instance of Parser
parser = Parser('intended\jpeg\save\path','intended\xmp\data\save\path')
# setting type of RAW files (currently only supports canon or sony)
parser.set_camera_type("canon")
# adding a folder to parser
parser.addFolder(r"A:\FolderPath\Example")
# can also add a list of folder paths
parse.addFolders([list_of_folder_paths])
# parsing XMP data into a pandas DataFrame
yourFrame = parser.parse()
# saving dataframe to intended data dir
parser.save()
```
### Converting RAW images to JPEG for use in keras
```python
from brycetools.images import converter

converter(r"Path\To\Pandas\Frame\MASTER.CSV")
# converter averages 3s/Photo
```