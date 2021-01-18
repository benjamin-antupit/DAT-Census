
#Library import
import pandas as pd
import numpy as np

def random_sample(df, sample_size = None, fraction = None, column = None):
    #Decision tree- parameters sample_size, fraction, and column are optional
    if column is None:
         #Will return entire row if user doesn't want a particular column
        if fraction is None:
             #Case 1: No fractional sample size parameter
            if sample_size is None:
                return df.sample() #Default- returns a random row
            else: #Numeric sample size has been provided
                return df.sample(n = sample_size)
        elif sample_size is None:
            #Case 2: No sample size provided
            return df.sample(frac = fraction) #No additional case bc we already know fraction has been provided due to the elif
        else:
            return None #all other cases
    else:
         #Replicated decision tree under here for case where column is provided
        if fraction is None:
            if sample_size is None:
                return df[column].sample() #All sample outputs here only provide samples of the user-specified column
            else:
                return df[column].sample(n = sample_size)
        elif sample_size is None:
            return df[column].sample(frac = fraction)
        else:
            return None
    
