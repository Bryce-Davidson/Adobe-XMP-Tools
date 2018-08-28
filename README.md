# brycetools
##### brycetools is a library built for preparing Adobe XMP data for training in keras

### The pipeline of this library is as follows:
##### 1) user_tools: Locate missing Data we need to generate
##### 2) apa: Create JPEG and Data dirctory's for saving (if preffered)
##### 3) parsing: Parse Files into a pandas DataFrame and save to disk
##### 4) images: Convert RAW files into JPEG's for Keras and append JPEG path to data row for Keras generator(AVG: 3s/Photo ) (if you have jpegs already converted with the same name as RAW files place them into the JPEG dir and images will see them)
##### 5) keras_tools: Load DataFrame from disk and shape accordingly for use in Model

### Parser
###### Parsing in bryctools is as simple as adding folder paths to an instance and calling a function
```python
from brycetools.parsing import Parser

# creating instance of class
# the Parser class takes two arguments
# a file path for intended JPEGS
parser = Parser('','')
# adding a folder path to instance
parser.addFolder(r"A:\FilePath\Example")
# parsing XMP data into a pandas DataFrame
dataFrame = parser.parse()
# saving dataframe to disk for later manipulation
```