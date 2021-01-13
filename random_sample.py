import pandas as pd
import numpy as np

def random_sample(df, sample_size = None, variable = None, fraction = None):
    if not variable:
        if not fraction:
            if not sample_size:
                return df.sample()
            else:
                return df.sample(size = sample_size)
        elif not sample_size:
            return df.sample(frac = fraction)
        else:
            return None
    else:
        if not fraction:
            if not sample_size:
                return df[variable].sample()
            else:
                return df[variable].sample(size = sample_size)
        elif not sample_size:
            return df[variable].sample(frac = fraction)
        else:
            return None
    
