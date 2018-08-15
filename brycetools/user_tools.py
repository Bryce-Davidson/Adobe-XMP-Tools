# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import os
from os import walk, listdir
from os.path import isfile, split
from pathlib import Path

#%%

"""
some ideas for this library:
    be able to take mulitple camera types and seperate accordingly
    in order to later sepearte the parsing into two types of cameras
    and dynamicly create more than one master frame at one time
"""
#%%

class FileOrganize:
    """
    fileOrganize is a class designed to help us with
    finding what data we have and what data we need to generate
    """
    def __init__(self):
        self.xmpExt = (".xmp",".XMP")
        self.folders = []
        self.camera_type = None    
        # might have to not store xmp in memory as they could be thousands
        self.xmp_paths = None
        # folders found after checking which xmp's we don't have
        self.missing_folders = None
        self.missing_cats = None

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
            
    def show_missing(self):
        if len(self.folders) == 0:
            raise ValueError("must add a folder")
        self.get_files()
        self.find_cats()
        return self.missing_cats
    
    # helper functions for get_file()    
    def remove_raw_add_xmp(self, paths: list)-> list:
        seperated = []
        for path in paths:
            name = path.split(".")[0]
            name += self.xmpExt[1]
            seperated.append(name)
        return seperated
    
    def find_missing_folders(self, xmpPaths: list):
        missing_folders = []
        for path in xmpPaths:
            if not isfile(path):
                missing_folder_path = split(path)[0]
                missing_folders.append(missing_folder_path)
        missing_folders = list(set(missing_folders))
        self.missing_folders = missing_folders
        
    def get_files(self):
        if self.camera_type is None:
            raise ValueError("must set camera type")
        if len(self.folders) == 0:
            raise ValueError("must add a folder")
        rawPaths = []
        for path in self.folders:
            for root, dirs, files in walk(path):
                for file in files:
                    if file.endswith(self.camera_type):
                        rawPaths.append(os.path.join(root, file))
        added_xmp = self.remove_raw_add_xmp(rawPaths)
        self.xmp_paths = added_xmp
        self.find_missing_folders(self.xmp_paths)

    def find_cats(self):
        cats = []
        folders = None
        for folder in self.missing_folders:
            for root, dirs, files in walk(folder):
                for file in files:
                    if file.endswith(".lrcat"):
                        cats.append(os.path.join(root, file))
        # if we don't have as many catalogs as we expected
        # find out what folders we need xmps for and get those paths
        if len(cats) < len(self.missing_folders):
            catsCompare = [split(split(path)[0])[0] for path in cats]
            folders = list(set(self.missing_folders) - set(catsCompare))
        generate_xmp_for = {
                'cats':cats,
                'folders': folders
                }
        self.missing_cats = generate_xmp_for
#%%
        
playPath = r"E:\parsingPlayground\showMissing"
organizer = FileOrganize()     
organizer.addFolder(playPath)
organizer.set_camera_type("canon")

mssing = organizer.show_missing()
    
#%%