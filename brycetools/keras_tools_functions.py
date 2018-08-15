import pandas as pd
import numpy as np
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from scipy import stats
from sklearn.preprocessing import MinMaxScaler
#%%
def pick_data(CSVPath: str, labelName: str) -> list:
    """
    from the csv pick the label you wan't to train on
    """
    data = pd.read_csv(CSVPath, index_col="image_id")
    data = data[[labelName, jpg_path]]
    data = data.dropna()
    data = np.array(data)
    return data    
#%%
def scale_frame(dataframe: list, labelName: str, feature_range=(0,1)):
    """
    takes a dataframe and removes the outliers
    feature scales all labelName values between 0,1
    """
    df_values = dataframe[[labelName]]
    df_paths = dataframe[["jpg_path"]]
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
    final_DF[[labelName]] = sc.fit_transform(final_DF[[labelName]])
    return final_DF
#%%
# helper function for keras_generator
    
def loadPhoto(imgPath: str)-> list:
    """
    loads photo into an image array with size (128, 128)
    """
    image = load_img(imgPath, target_size=(128, 128))
    image = img_to_array(image)
    return image