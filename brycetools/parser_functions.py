# -*- coding: utf-8 -*-
import os
import xmltodict
import pandas as pd
import collections
import os
import sys
from os import walk
from os import listdir

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
def get_file_type(brand: str):
    brand = brand.lower()
    fileType = []
    if brand == "canon":
        fileType = [".cr2", ".CR2"]
    elif brand == "sony":
        fileType = [".arw",".ARW"]
    return tuple(fileType)
#%%
def get_files(folderPaths: list, fileType: tuple)-> list:
    # TODO: throw error if folderPaths is not list
    
    """
    takes in a list of folders or a single 
    folder and returns lists of those files
    
    folderPaths:
        contains string paths of the folders or folder you
        would like to locate files in
        
    fileType:
        contains the camera brands file extensions
        (can be recieved by calling get_file_type())
        
    Returns:
        returns a list of .xmp and .raw file paths
    """
    if isinstance(folderPaths, list):
        xmpExt = (".xmp",".XMP")
        xmpPaths = []
        rawPaths = []
        for path in folderPaths:
            for root, dirs, files in walk(path):
                for file in files:
                    if file.endswith(xmpExt):
                        xmpPaths.append(os.path.join(root, file))
                    elif file.endswith(fileType):
                        rawPaths.append(os.path.join(root, file))
    else:
        raise ValueError("expected LIST got {}".format(type(folderPaths)))
    return [xmpPaths, rawPaths, fileType]
#%%
def file_match(removedXmp: list, removedRaw: list, cameraType: tuple) -> list:
    """
    takes in lists of paths with file extensions removed
    and finds matching pairs of xmp's and raws
    
    seperatedXmp:
        a list of xmp paths with the extension removed using
        seperate_paths()
    seperatedRaw:
        a list of raw paths withthe extension removed using
        seperate_paths
    """
    inBothLists = list(set(removedXmp).intersection(removedRaw))
    inBoth = []
    for file in inBothLists:
        xmp = file + ".XMP"
        raw = file + cameraType[1]
        inBoth.append([xmp, raw])
    return inBoth


def remove_ext(paths: list)-> list:
    """
    takes in a list of paths and removes the file extenion
    
    paths:
        a list of file paths
    """
    seperated = []
    for path in paths:
        name = path.split(".")[0]
        seperated.append(name)
    return seperated
#%%
def organize_files(files: list)-> list:
    """
    takes a list conatinaing file paths and returns pairs
    list of file paths can be recieved by calling get_files()
    expects shape given by get_files()
    
    expects shape [xmpPaths, rawPaths, cameraType]
    filePaths: 
        a list of file paths with shape [[xmpPaths], [rawPaths]]
    Returns:
        returns a list of file paths in both lists
    """
    xmpPaths = files[0]
    rawPaths = files[1]
    cameraType = files[2]
    xmpNames = remove_ext(rawPaths)
    rawNames = remove_ext(xmpPaths)
    matched = file_match(xmpNames, rawNames, cameraType)
    return matched
#%%    
def flattenDict(d: dict, parent_key='', sep='_') -> dict:
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flattenDict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)
#%%
def parse_xmp(organizedPaths: list, jpg_dir: str)-> list:
    """
    takes in a list of xmps, creates a dataframe and saves as CSV
    
    oranizedPaths:
        a list of xmp paths
    """
    parsedXMPDicts = []
    for xmp, raw in organizedPaths:
        xmp = open(xmp)
        readXmp = xmp.read()
        xmp.close()
        parsed = xmltodict.parse(readXmp)
        needed = parsed["x:xmpmeta"]["rdf:RDF"]["rdf:Description"]
        needed["raw_path"] = raw
        needed["jpg_dir"] = jpg_dir
        try:
            fileName = needed["@crs:RawFileName"].split(".")[0]
            needed["image_id"] = fileName
        except KeyError:
            print("{} has been omitted".format(raw))
            pass
            continue
        finalDict = flattenDict(needed, parent_key="", sep=":")
        parsedXMPDicts.append(finalDict)
    MASTER = pd.DataFrame(parsedXMPDicts)
    MASTER.set_index("image_id", inplace=True)
    return MASTER
#%%    
def loop_parse_xmp(lop: list) -> list:
    """
    takes in a list of paths (lop) and returns list of parsed xmp dicts
    """
    parsedXMPDicts = []
    for filePath in lop:
        file = open(filePath)
        fileRead = file.read()
        file.close()
        parsed = xmltodict.parse(fileRead)
        needed = parsed["x:xmpmeta"]["rdf:RDF"]["rdf:Description"]
        try:
            fileName = parsed["x:xmpmeta"]["rdf:RDF"]["rdf:Description"]["@crs:RawFileName"].split(".")[0]
            needed["image_id"] = fileName    
        except KeyError:
            pass
            continue
        finalDict = flattenDict(needed, parent_key="", sep=":")
        parsedXMPDicts.append(finalDict)
    #list of flattened dicts
    return parsedXMPDicts

def singleFileParse(filePath):
    """
    takes in single file path and returns parsed XMP dict
    """
    file = open(filePath)
    fileRead = file.read()
    file.close()
    parsed = xmltodict.parse(fileRead)
    needed = parsed["x:xmpmeta"]["rdf:RDF"]["rdf:Description"]
    fileName = needed["@crs:RawFileName"].split(".")[0]
    try:
        fileName = parsed["x:xmpmeta"]["rdf:RDF"]["rdf:Description"]["@crs:RawFileName"].split(".")[0]
        needed["image_id"] = fileName    
    except KeyError:
        pass
    finalDict = flattenDict(needed, parent_key="", sep=":")
    return finalDict
