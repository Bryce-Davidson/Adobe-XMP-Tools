# -*- coding: utf-8 -*-
import rawpy
import imageio
from os.path import join
from tqdm import tqdm
#%%
def raw_to_jpg(masterCSVPath: str):
    # dataFrame = pd.read_csv(masterCSVPath, index_col="image_id")
    # the below line is used for testing when dataframe is loaded into memory
    dataFrame = masterCSVPath
    dfLength = len(dataFrame.index)
    for index, rows in tqdm(dataFrame.iterrows(), total=dfLength, unit="Photos"):
        rawPath = dataFrame.at[index, "raw_path"]
        jpgDir = dataFrame.at[index, "jpg_dir"]
        fileName = index + ".jpg"
        savePath = join(jpgDir, fileName)
        # adds the path where we save it, usually handled by the dataframe
        # at the start
        dataFrame.at[index, "jpg_save_path"] = savePath
        with rawpy.imread(rawPath) as raw:
            rgb = raw.postprocess()
            imageio.imsave(savePath, rgb)      
raw_to_jpg(master_final)        
#%%%







