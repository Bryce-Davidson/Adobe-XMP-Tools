# -*- coding: utf-8 -*-
from os.path import join, isdir
from os import makedirs, mkdir, listdir
#%%
def folderStruct(location: str)-> list:
    """
    Creates a fresh folder structure on a new systyem

    Returns:
        jpg_directory path
        Data_directory path

        to be used with the parsing module
    """
    apaFolder = location + "\APA"
    if not isdir(apaFolder):
        subs = [apaFolder + r"\JPG", apaFolder + r"\Data"]
        mkdir(apaFolder)
        for sub in subs:
            makedirs(join(apaFolder, sub))
    else:
        paths = listdir(apaFolder)
        jpgPath = join(apaFolder, paths[0])
        dataPath = join(apaFolder, paths[1])
        return [jpgPath, dataPath]
        raise ValueError("Folder already exists")
    return [subs[0], subs[1]]
#%%
