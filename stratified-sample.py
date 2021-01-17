import pandas as pd
import numpy as np
import random_sample
import sample_import


def stratified_sample(df, column):
    #Data
    gender = {"Female":243/472, "Male":212/472, "Other":17/472}
    race = {"American Indian or Alaska Native":4/472,"Asian":231/472}

    #empty list to store dfSlices
    dfSlices = [0] * len(df.columns)
    i = 0

    #breaks up slices by column parameter, stores them in empty list
    for region, df_region in df.groupby(column):
        dfSlices[i] = df_region
        i += 1

    #determines where to search for the percentages for each bucket
    if lower(column) == "gender": size = gender
    elif lower(column) == "Race": size = race

    #creates list of the buckets
    slices = [random_sample(dfSlice, len(dfSlice.index) * size[dfSlice[column].iloc[0]]) for dfSlice in dfSlices]

    #sticks them together, returns
    return pd.concat(slices)
