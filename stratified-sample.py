import pandas as pd
import numpy as np
import random_sample


def stratified_sample(df, column, n, weights=None):
    if not weights:
        weights = {}
        values = df[column].unique()

        for value in values:
            weights[value] = 1 / len(values)

    l = [0] * len(df.columns)
    i = 0
    rows = len(df.index)

    for region, df_region in df.groupby(column):
        l[i] = df_region
        i += 1

    slices = [pfSlice.random_sample(len(pfSlice.index) // size) for pfSlice in l]
    df_final = pd.concat(slices)
