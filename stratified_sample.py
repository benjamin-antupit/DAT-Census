import pandas as pd
import numpy as np
from random_sample import random_sample


def stratified_sample(df, column, n):

    #Remove, temporary solution to the issue of dealing with mixed differnt than the DEI survey
    df.drop(df.tail(1).index,inplace=True)
    #Data
    #At some point, this would be great as an import, however at this time the file is not computer readable so hardcode is faster
    #Non-Binary -- No Data
    #Prefer not to say -- No data
    gender = {"Female":243/472, "Male":212/472, "Other":17/472,"Prefer not to say":0,"Non-binary":0}
    #Remove East Asian tester
    #Indian -- No data
    race = {"American Indian or Alaskan Native":4/472,"Indian":0/472,"East Asian":231/472,"Other Asian":231/472,"Black or African American":20/472,"Hispanic or Latino":45/472,"Middle Eastern":15/472,"Multiracial":61/472,"Native Hawaiian or Other Pacific Islander":15/472,"White":203/472,"Other":16/472,"I prefer not to respond":19/472}
    grade = {6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0}

    #empty list to store dfSlices
    dfSlices = []

    #breaks up slices by column parameter, stores them in empty list
    for df_region in df.groupby(by=[column]).__iter__():
        dfSlices.append(df_region)


    #determines where to search for the percentages for each bucket
    if column == "Q22 (What is your gender identity? - Selected Choice)": size = gender
    elif column == "Q23 (What is your grade level?)": size = grade
    elif column == "Q24 (What is your racial or ethnic identification? (select all that apply))": size = race


    #creates list of the buckets
    slices = [random_sample(dfSlice[1], round(n * size[dfSlice[1][column].iloc[0]])) for dfSlice in dfSlices]

    #sticks them together, returns
    return pd.concat(slices)
