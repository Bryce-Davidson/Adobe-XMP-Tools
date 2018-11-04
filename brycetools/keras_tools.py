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
        self.dataFrame = pd.read_csv(csvPath, index_col="image_id")
        
        self.labeled = None
        self.jpgPaths = None
        self.converted = None    
        self.scaled = None
        self.prepared = None
        self._labels = [ predictLabel,
                          "@exif:ExposureTime",
                          "@exif:ApertureValue",
                          "@exif:ExposureProgram",
                          "@exif:RecommendedExposureIndex",
                          "@exif:MaxApertureValue",
                          "@exif:MeteringMode",
                          "@exif:FocalLength",
                          "@exif:ExposureMode",
                          "@exif:WhiteBalance",
                          "@aux:LensID",
                          "exif:ISOSpeedRatings:rdf:Seq:rdf:li",
                          ]

    def prepare(self):
        self._pick()
        self._convert_fractions()
        self._scale()
        self._align()
        return self.prepared
    
    def reset_predict_label(self, newLabel: str):
        self._labels[0] = newLabel
        self.prepare()
    
    def _pick(self):
        self.labeled = self.dataFrame[self._labels]
        self.jpgPaths = self.dataFrame.jpg_save_path
        self.jpgPaths = self.jpgPaths.reset_index(inplace=False, level=0)
         
    def _convert_fractions(self):
        self.converted = self.labeled.applymap(self.frac_to_dec)
        self.converted = self.converted.fillna(0)
        
    def _scale(self):
        sc = MinMaxScaler(feature_range=(0,1))
        scaledData = sc.fit_transform(self.converted[self._labels])
        self.scaled = pd.DataFrame(scaledData)
    
    def _align(self):
        self.prepared = pd.concat([self.scaled, self.jpgPaths], axis=1)
   
    @staticmethod
    def frac_to_dec(s):
        if s == np.nan:
            return np.nan
        try:
            return float(s)
        except ValueError:
            num, denom = s.split('/')
            return float(num) / float(denom)


def loadPhoto(imgPath: str)-> list:
    image = load_img(imgPath, target_size=(224, 224))
    image = img_to_array(image)
    return image

def keras_apa_generator(dataArray: list, batch_size = 10):
    while True:
          # select random indexes(rows) for batch
          batch = dataArray[np.random.randint(0, dataArray.shape[0],batch_size)]
          batch_input = []
          batch_output = []
          batch_otherInput = []
          for row in batch:
              #inputImg = loadPhoto(os.path.join(r"DATA/DIR" + dataArray[1,12]))
              inputImg = loadPhoto(row[14])
              otherInput = row[1:12]
              outputValue = row[0]
              batch_input += [ inputImg ]
              batch_otherInput += [ otherInput ]
              batch_output += [ outputValue ]
          # Return a tuple of (input,output) to feed the network
          batch_other = np.array( batch_otherInput )
          batch_x = np.array( batch_input )
          batch_y = np.array( batch_output )
          yield ({'image_input': batch_x , 'aux_input': batch_other}, {'prediction': batch_y})
