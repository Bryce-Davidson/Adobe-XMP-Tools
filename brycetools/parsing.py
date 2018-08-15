# -*- coding: utf-8 -*-
import os
import xmltodict
import pandas as pd
import collections
import os
import sys
from os import walk
from os import listdir

# mainPath = r"C:\Users\Bryce\Dropbox\Automatic Photograph Adjuster\Code\Bryce"
# playPath = r"E:\parsingPlayground\showMissing\raw-Ncat-Nxmp"
# jpg_path, data_path = struct(mainPath)


#%%
"""
please take note, in spyder if you import these functions
you may press CTRL + i on any function to learn more about it

the general pipeline of the program should go:
    
    get_file_type() -> to get the tuple of possible extensions for the raw files(sony, canon)
    get_files() -> to get lists of paths relating to xmps and raws
    organize_files() -> to make sure we have both [[xmpPath], & [raw_Path]] 
    parse_xmp() -> to parse xmp files into a dataframe to save as CSV
    save_dataframe() -> to save dataframe into csv for data flow module

    thus will conclude this modules pipeline
    -> next up will be the images.py module and then keras_tools 
"""
#%%
# this parser is an easy to use wrapping of the parsing
# functions I have written below
# TODO be able to take multiple camera types and create dataframes accordingly
# this will require having to chnage the struct command with dynamic input as well
class Parser: 
    
    def __init__(self, jpg_dir, data_dir):
        self.jpg_dir = jpg_dir
        self.data_dir = data_dir
        
        self.folders = []
        self.camera_type = []
        self.files = None
        self.organized = None
        # self.checkslots = None
    def set_camera_type(self, brand: str):
        brand = brand.lower()
        if brand == "canon":
            self.camera_type = tuple([".cr2", ".CR2"])
        elif brand == "sony":
            self.camera_type = tuple([".arw",".ARW"])
            
    def addFolder(self, folder: str):
        self.folders.append(folder)
        
    def addFolders(self, folders: list):
        for folder in folders:
            self.folders.append(folder)
                    
    def parse(self):
        files = self.get_files()
        organized = self.organize_files()
        parsed = self.parse_xmp()
        return parsed
        
    def get_files(self):
        if len(self.camera_type) == 0:
            raise ValueError("must set camera type")
        if len(self.folders) == 0:
            raise ValueError("must add a folder")
        xmpExt = (".xmp",".XMP")
        xmpPaths = []
        rawPaths = []
        for path in self.folders:
            for root, dirs, files in walk(path):
                for file in files:
                    if file.endswith(xmpExt):
                        xmpPaths.append(os.path.join(root, file))
                    elif file.endswith(self.camera_type):
                        rawPaths.append(os.path.join(root, file))
        self.files = [xmpPaths, rawPaths]
        
    # helper functions for organize files --> will clean up after
    def file_match(self, removedXmp: list, removedRaw: list) -> list:
        inBothLists = list(set(removedXmp).intersection(removedRaw))
        inBoth = []
        for file in inBothLists:
            xmp = file + ".XMP"
            raw = file + self.camera_type[1]
            inBoth.append([xmp, raw])
        return inBoth
    
    def remove_ext(self, paths: list)-> list:
        seperated = []
        for path in paths:
            name = path.split(".")[0]
            seperated.append(name)
        return seperated
    
    def organize_files(self)-> list:
        xmpPaths = self.files[0]
        rawPaths = self.files[1]
        xmpNames = self.remove_ext(rawPaths)
        rawNames = self.remove_ext(xmpPaths)
        matched = self.file_match(xmpNames, rawNames)
        self.organized = matched
        
    def flattenDict(self, d: dict, parent_key='', sep='_') -> dict:
        items = []
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, collections.MutableMapping):
                items.extend(self.flattenDict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)
    
    def parse_xmp(self):
        parsedXMPDicts = []
        for xmp, raw in self.organized:
            xmp = open(xmp)
            readXmp = xmp.read()
            xmp.close()
            parsed = xmltodict.parse(readXmp)
            needed = parsed["x:xmpmeta"]["rdf:RDF"]["rdf:Description"]
            needed["raw_path"] = raw
            needed["jpg_dir"] = self.jpg_dir
            try:
                fileName = needed["@crs:RawFileName"].split(".")[0]
                needed["image_id"] = fileName
            except KeyError:
                print("{} has been omitted".format(xmp))
                pass
                continue
            finalDict = self.flattenDict(needed, sep=":")
            parsedXMPDicts.append(finalDict)
        master = pd.DataFrame(parsedXMPDicts)
        master.set_index("image_id", inplace=True)
        return master
#%%