import pandas as pd
import numpy as np

def weighted_sample(df, column, weights, n):
    indexWeights = []
    counts = df[column].value_counts()
    
    for key in weights:
        weights[key] = weights[key]/counts[key]

    for row in df.index:
        indexWeights.append(weights[df[column][row]])

    return df.sample(n, weights=indexWeights)
