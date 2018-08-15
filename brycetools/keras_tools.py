# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from scipy import stats
from sklearn.preprocessing import MinMaxScaler
#%%
class PrepareData:
    
    def __init__(self, csvPath: str, labelName: str):
        self.csvPath = csvPath
        self.labelName = labelName
        self.dataFrame = pd.read_csv(self.csvPath, index_col="image_id")
        self.pickedData = None
        self.scaledData = None
        self.prepared = None
        
    def prepare_data(self):
        self.pick_data_col()
        prepared = self.scale_frame()
        self.prepared = prepared
        return self.prepared
    
    def pick_data_col(self) -> list:
        data = self.dataFrame
        data = data[[self.labelName, jpg_path]]
        data = data.dropna()
        data = np.array(data)
        self.pickedData = data

    def scale_frame(self, feature_range=(0,1)):
        df_values = self.dataFrame[[self.labelName]]
        df_paths = self.dataFrame[["jpg_save_path"]]
        # remove outliers
        df_values = df_values[(np.abs(stats.zscore(df_values)) < 3).all(axis=1)]
        # join the outliers removed frame and the path frame together again by index
        final_DF = pd.concat([df_values, df_paths], axis=1)
        # delete undeeded frames from memory
        del df_values
        del df_paths
        # drop all empty data from final frame
        final_DF = final_DF.dropna()        
        # scale values in final frame
        sc = MinMaxScaler(feature_range=feature_range)
        final_DF[[self.labelName]] = sc.fit_transform(final_DF[[self.labelName]])
        self.scaledData = final_DF
#%%
def keras_image_generator(dataArray: list, batch_size = 10):
# TODO: make it so this can take more than one y value    
    """
    takes in numpy data array from scale_frame 
    expected shape = [value, imgPath]
    """
    while True:
          # select random indexes(rows) for batch
          batch_paths = dataArray[np.random.randint(0,dataArray.shape[0],batch_size)]
          # create pyhton arrays
          batch_input = []
          batch_output = []
          # Read row, load the photo and take the value
          for value, filepath in batch_paths:
              inputImg = loadPhoto(filepath)
              inputImg /= 255
              outputValue = value
            # appending values and photos into python arrays
              batch_input += [ inputImg ]
              batch_output += [ outputValue ]
          # Return a tuple of (input,output) to feed the network
          batch_x = np.array( batch_input )
          batch_y = np.array( batch_output )
        
          yield( batch_x, batch_y )