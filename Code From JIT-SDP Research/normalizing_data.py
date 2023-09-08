# import pandas as pd
import math
# import numpy as np
from scipy.stats import yeojohnson
import get_data_and_statistics as gds

def fan2019_normilization(df):
    null_count = 0
    for attribute in gds.UNIFORM_ATTRIBUTES:
        try:
            df[attribute] = df[attribute].apply(lambda x: math.log(x + 1))
            # '_' holds second output, a scalar used to restore data to its original state
            df[attribute], _ = yeojohnson(df[attribute]) # great for rexp
            # little effect - df[attribute], _ = boxcox(df[attribute])
            # df[attribute] = 1/df[attribute]
            
        except ValueError:
            null_count += 1
    print(null_count, " grrr so many blanks")

def catolino2019_normalization(df):
    # replacing any null values with the median of the respective column
    medians = df.median()
    # print(medians)
    df.fillna(value=medians, inplace=True)
    """
    null_count = 0
    for attribute in gds.UNIFORM_ATTRIBUTES:
        try:
            df[attribute] = df[attribute].apply(lambda x: math.log(x + 1))
            # '_' holds second output, a scalar used to restore data to its original state
            df[attribute], _ = yeojohnson(df[attribute]) # great for rexp
            # little effect - df[attribute], _ = boxcox(df[attribute])
            # df[attribute] = 1/df[attribute]
            
        except ValueError:
            null_count += 1
    print(null_count, " grrr so many blanks")
    """
    
    
def kamei2012_normalization(df):
    for attribute in gds.UNIFORM_ATTRIBUTES:
        df[attribute], _ = yeojohnson(df[attribute])
    
def mcintosh2017_normilization(df):
    df['bug'].fillna(value=0, inplace=True)
    # replacing any null values with the median of the respective column
    medians = df.median()
    # print(medians)
    df.fillna(value=medians, inplace=True)
    for attribute in gds.UNIFORM_ATTRIBUTES:
        df[attribute], _ = yeojohnson(df[attribute])


