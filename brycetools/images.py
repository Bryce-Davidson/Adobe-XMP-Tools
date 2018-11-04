import numpy as np
import pandas as pd
import rawpy
import imageio
from tqdm import tqdm
from scipy.misc import imresize
from os.path import join, isfile
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
import datetime

def convert(masterCSVPath: str):
    """
    Converts RAW photos into JPEGS
    Args:
        masterCSVPath: path of DataFrame created by Parser class

    """
    dataFrame = pd.read_csv(masterCSVPath, index_col="image_id")
    dataFrame["jpg_save_path"] = "nan"

    dfLength = len(dataFrame.index)
    counter = 0
    for index, cols in tqdm(dataFrame.iterrows(), total=dfLength, unit="Photo"):
        counter += 1
        if counter % 10 == 0:
            print(datetime.datetime.now())
        
        rawPath = cols["raw_path"]
        jpgDir = cols["jpg_dir"]

        fileName = index + ".jpg"

        savePath = join(jpgDir, fileName)
        if isfile(savePath) == True:
            dataFrame.at[index, "jpg_save_path"] = savePath
            continue
        cols["jpg_save_path"] = savePath

        with rawpy.imread(rawPath) as raw:
            rgb = raw.postprocess()
            rgb = imresize(rgb, (64,64))
            imageio.imsave(savePath, rgb)

    dataFrame.to_csv(masterCSVPath)

def resize(array):
    paths = array[:, 12:]
    for name, path in tqdm(paths):
        root = r"E:\APA\Resized"
        fileName = name + ".jpg"
        savePath = join(root, fileName)
        image = load_img(path, target_size=(64, 64))
        image = img_to_array(image)
        imageio.imsave(savePath, image)
