# brycetools
###### brycetools is a library built for preparing Adobe XMP data for training in keras

### Parser
"""python
from brycetools.parsing import Parser

# creating instance of class
parser = Parser()
# adding a folder path to instance
parser.addFolder(r"A:\FilePath\Example")
# parsing XMP data into a pandas DataFrame
dataFrame = parser.parse()
"""