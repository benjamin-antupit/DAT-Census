import pandas as pd
import numpy as np

def random_sample(df, sample_size = None, fraction = None, column = None):
    if column is None:
        if fraction is None:
            if sample_size is None:
                return df.sample()
            else:
                return df.sample(n = sample_size)
        elif sample_size is None:
            return df.sample(frac = fraction)
        else:
            return None
    else:
        if fraction is None:
            if sample_size is None:
                return df[column].sample()
            else:
                return df[column].sample(n = sample_size)
        elif sample_size is None:
            return df[column].sample(frac = fraction)
        else:
            return None
    
