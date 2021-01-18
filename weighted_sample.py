import pandas as pd
import numpy as np

def weighted_sample(df, column, n, weights=None):
    if not weights:
        #weight each distinct value in column equally
        weights = {}
        values = df[column].unique() #list of all distinct values in the column
        for value in values:
            weights[value] = 1/len(values)
        
    indexWeights = [] #weights of individual responses
    counts = df[column].value_counts() #series with number of occurences of each value
    
    for key in weights:
        weights[key] = weights[key]/counts[key] #total weight of all rows with value key will be the original weight[key]

    #each row is assigned the appropriate weight
    for row in df.index:
        indexWeights.append(weights[df[column][row]])

    return df.sample(n, weights=indexWeights)
