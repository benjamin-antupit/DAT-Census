import pandas as pd
import numpy as np
from random_sample import random_sample


def stratified_sample(df, column, n=None, fraction = None):
    if not n:
        n = round(fraction * len(df))

    #temporary solution until more data on mixed is recieved
    if column == "Q24":
        df.loc[df['Q24'].str.contains(','), 'Q24'] = 'Multiracial'

    #Remove, temporary solution to remove the 1 mixed response until they change their survey to just say mixed
    #df.drop(df.tail(1).index,inplace=True)
    #Data
    #At some point, this would be great as an import, however at this time the file is not computer readable so hardcode is faster
    #Non-Binary -- No Data
    #Prefer not to say -- No data
    gender = {"Female":243/472, "Male":212/472, "Other":17/472,"Prefer not to say":0,"Non-binary":0}
    #Remove East Asian tester
    #Indian -- No data
    race = {"American Indian or Alaskan Native":4/472,"Indian":0/472,"East Asian":231/472,"Other Asian":231/472,"Black or African American":20/472,"Hispanic or Latino":45/472,"Middle Eastern":15/472,"Multiracial":61/472,"Native Hawaiian or Other Pacific Islander":15/472,"White":203/472,"Other":16/472,"I prefer not to respond":19/472}
    #Missing all data
    grade = {6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0}

    #empty list to store dfSlices
    dfSlices = []

    #breaks up slices by column parameter, stores them in empty list
    for df_region in df.groupby(by=[column]).__iter__():
        if df_region[1][column].iloc[0] != "":
            dfSlices.append(df_region)

    #determines where to search for the percentages for each bucket
    if column == "Q22": size = gender
    elif column == "Q23": size = grade
    elif column == "Q24": size = race

    #creates list of the buckets
    try:
        slices = [random_sample(dfSlice[1], sample_size=round(n * size[dfSlice[1][column].iloc[0]])) for dfSlice in dfSlices]

    except ValueError: 
        print("Not enough datapoints.")
        return pd.DataFrame({})

    #sticks them together, returns
    return pd.concat(slices)
