import pandas as pd
import numpy as np

def random_sample(df, sample_size = None, fraction = None, column = None):
    if not column:
        if not fraction:
            if not sample_size:
                return df.sample()
            else:
                return df.sample(n = sample_size)
        elif not sample_size:
            return df.sample(frac = fraction)
        else:
            return None
    else:
        if not fraction:
            if not sample_size:
                return df[column].sample()
            else:
                return df[column].sample(size = sample_size)
        elif not sample_size:
            return df[column].sample(frac = fraction)
        else:
            return None
    
