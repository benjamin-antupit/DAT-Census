import pandas as pd
import math


def random_sample(df, sample_size: int = None, fraction: float = None, column: str = None) -> pd.DataFrame:
    # Decision tree- parameters sample_size, fraction, and column are optional
    if column is None:
        # Will return entire row if user doesn't want a particular column
        if fraction is None:
            # Case 1: No fractional sample size parameter
            if sample_size is None:
                return df.sample()  # Default- returns a random row
            else:  # Numeric sample size has been provided
                return df.sample(n=sample_size)
        elif sample_size is None:
            # Case 2: No sample size provided
            return df.sample(
                frac=fraction)  # No additional case bc we already know fraction has been provided due to the elif
        else:
            return df  # all other cases
    else:
        # Replicated decision tree under here for case where column is provided
        if fraction is None:
            if sample_size is None:
                return df[column].sample()  # All sample outputs here only provide samples of the user-specified column
            else:
                return df[column].sample(n=sample_size)
        elif sample_size is None:
            return df[column].sample(frac=fraction)
        else:
            return df


def stratified_sample(df: pd.DataFrame, column: str, n: int = None, fraction: float = None) -> pd.DataFrame:
    # transforming fraction to number of data points if necessary
    if not n:
        n = round(fraction * len(df))

    '''
    Temporary solution until more data on mixed is received as we have no data on each "bucket" of multiracial
    Easier to just bucket them together in the meantime until further data is received
    '''
    if column == "Q24":
        df.loc[df['Q24'].str.contains(','), 'Q24'] = 'Multiracial'

    '''
    All Data
    At some point, this would be great as an import, however the file is not computer-readable so hardcode is faster
    Non-Binary -- No Data
    Prefer not to say -- No data
    '''
    gender = {"Female": 243 / 472, "Male": 212 / 472, "Other": 17 / 472, "Prefer not to say": 0, "Non-binary": 0}
    '''
    #East Asian was old wording, was updated to Other Asian. Remove East Asian once we get full dataset
    #Indian -- No data
    '''
    race = {"American Indian or Alaskan Native": 4 / 472, "Indian": 0 / 472, "East Asian": 231 / 472,
            "Other Asian": 231 / 472, "Black or African American": 20 / 472, "Hispanic or Latino": 45 / 472,
            "Middle Eastern": 15 / 472, "Multiracial": 61 / 472, "Native Hawaiian or Other Pacific Islander": 15 / 472,
            "White": 203 / 472, "Other": 16 / 472, "I prefer not to respond": 19 / 472}

    # Missing all data
    grade = {6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}

    # empty list to store dfSlices
    dfSlices = []

    # breaks up slices by column parameter, stores them in empty list
    for df_region in df.groupby(by=[column]).__iter__():
        if df_region[1][column].iloc[0] != "":
            dfSlices.append(df_region)

    # determines where to search for the percentages for each bucket
    if column == "Q22":
        size = gender
    elif column == "Q23":
        size = grade
    elif column == "Q24":
        size = race

    # creates list of the buckets
    try:
        slices = [random_sample(dfSlice[1], sample_size=round(n * size[dfSlice[1][column].iloc[0]])) for dfSlice in
                  dfSlices]

    # if it needs more data points from a bucket than there actually are
    except ValueError:
        print("Not enough data points.")
        return df
    except NameError:
        print("No demographics beyond Q22, Q23, and Q24")
        return df
    # sticks them together, returns
    return pd.concat(slices)


def weighted_sample(df: pd.DataFrame, column: str, n: int = None,
                    frac: float = None, weights: dict = None) -> pd.DataFrame:
    if not n and not frac:
        return pd.DataFrame()
    if not n:
        n = math.floor(len(df.index) * frac)

    if not weights:
        # weight each distinct value in column equally
        weights = {}
        values = df[column].unique()  # list of all distinct values in the column
        for value in values:
            weights[value] = 1 / len(values)

    indexWeights = []  # weights of individual responses
    counts = df[column].value_counts()  # series with number of occurrences of each value

    for key in weights:
        weights[key] = weights[key] / counts[
            key]  # total weight of all rows with value key will be the original weight[key]

    # each row is assigned the appropriate weight
    for row in df.index:
        indexWeights.append(weights[df[column][row]])

    return df.sample(n, weights=indexWeights)
