# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import rawpy
import imageio
from os.path import join, isfile
from tqdm import tqdm
#%%
def raw_to_jpg(masterCSVPath: str):
    dataFrame = pd.read_csv(masterCSVPath, index_col="image_id")
    # the below line is used for testing when dataframe is loaded into memory
    dfLength = len(dataFrame.index)
    counter = 0
    for index, cols in tqdm(dataFrame.iterrows(), total=dfLength, unit="Photo"):
        # every 10 photos save the data frame
        counter += 1
        if counter % 100 == 0:
            dataFrame.to_csv(masterCSVPath)
        # allow my bitch ass laptop to cool down
        if counter % 7193 == 0:
            break
        rawPath = cols["raw_path"]
        jpgDir = cols["jpg_dir"]
        fileName = index + ".jpg"
        savePath = join(jpgDir, fileName)
        # if file already exists skip the file and add the filepath to dataFrame
        if isfile(savePath) == True:
            cols["jpg_save_path"] = savePath
            continue
        cols["jpg_save_path"] = savePath
        with rawpy.imread(rawPath) as raw:
            rgb = raw.postprocess()
            imageio.imsave(savePath, rgb)
    dataFrame.to_csv(masterCSVPath)
#%%%
raw_to_jpg(r"E:\APA\Data\JM-MASTER.CSV")


#%%
dataFrame = pd.read_csv(r"E:\APA\Data\JM-MASTER.CSV", index_col="image_id")

        
        
        
        
        
        
        
        