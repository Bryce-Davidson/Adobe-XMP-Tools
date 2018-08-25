# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from scipy import stats
from sklearn.preprocessing import MinMaxScaler
#%%
class PrepareData:
    
    def __init__(self, csvPath: str, predictLabel: str):
        self.indLabels = [ predictLabel,
                          "@exif:ExposureTime",
                          "@exif:ApertureValue",
                          "@exif:ExposureProgram",
                          "@exif:SensitivityType",
                          "@exif:RecommendedExposureIndex",
                          "@exif:ExposureBiasValue",
                          "@exif:MaxApertureValue",
                          "@exif:MeteringMode",
                          "@exif:FocalLength",
                          "@exif:ExposureMode",
                          "@exif:WhiteBalance",
                          "@exif:SceneCaptureType",
                          "@aux:LensID",
                          "@aux:ApproximateFocusDistance",
                          "exif:ISOSpeedRatings:rdf:Seq:rdf:li" ]
        self.csvPath = csvPath
        self.predictLabel = predictLabel
        self.dataFrame = pd.read_csv(self.csvPath, index_col="image_id")
        self.pickedData = self.dataFrame[self.indLabels]
        self.converted = self.pickedData.applymap(self.frac_to_dec)
        self.scaledData = None
        self.prepared = None
    
    @staticmethod
    def frac_to_dec(s):
        try:
            return float(s)
        except ValueError:
            num, denom = s.split('/')
            return float(num) / float(denom)
   
    def scale_data(self):
        sc = MinMaxScaler(feature_range=(0,1))
        self.scaledData = sc.fit_transform(self.converted[self.indLabels])
    
    # will have to rewrite to include extra variables

#%%
def keras_image_generator_multiple(dataArray: list, batch_size = 10):
    while True:
          # select random indexes(rows) for batch
          batch = dataArray[np.random.randint(0,dataArray.shape[0],batch_size)]
          # create pyhton arrays
          batch_input = []
          batch_output = []
          batch_input2 = []
          # Read row, load the photo and take the value
          for row in batch:
              inputImg = loadPhoto(row[16])
              inputImg /= 255
              secondInput = row[1:16]
              outputValue = row[0]
            # appending values and photos into python arrays
              batch_input += [ inputImg ]
              batch_input2 += [ secondInput ]
              batch_output += [ outputValue ]
          # Return a tuple of (input,output) to feed the network
          batch_second_x = np.array( batch_input2 )
          batch_x = np.array( batch_input )
          batch_y = np.array( batch_output )
        
          yield( batch_x, batch_y, batch_second_x )

    
#%%
def keras_image_generator_single(dataArray: list, batch_size = 10):
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