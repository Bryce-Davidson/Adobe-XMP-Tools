# brycetools
#### brycetools is a library built for preparing Adobe XMP data for training in keras
---
### Parsing XMP files into Pandas DataFrame
```python
from brycetools.parsing import Parser

# creating instance of Parser
parser = Parser('intended\jpeg\save\path','intended\data\save\path')
# adding a folder to parser
parser.addFolder(r"A:\FolderPath\Example")
# parsing XMP data into a pandas DataFrame
yourFrame = parser.parse()
# saving dataframe to intended data dir
parser.save()
```
### Converting Raw images