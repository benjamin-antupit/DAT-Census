import pandas as pd


def random_sample(df, n: int = None, percent: float = None, column: str = None) -> pd.DataFrame:
    # Decision tree- parameters sample_size, fraction, and column are optional
    if column is None:
        # Will return entire row if user doesn't want a particular column
        if percent is None:
            # Case 1: No fractional sample size parameter
            if n is None:
                return df.sample()  # Default- returns a random row
            else:  # Numeric sample size has been provided
                return df.sample(n=n)
        elif n is None:
            # Case 2: No sample size provided
            return df.sample(
                frac=percent)  # No additional case bc we already know fraction has been provided due to the elif
        else:
            return df  # all other cases
    else:
        # Replicated decision tree under here for case where column is provided
        if percent is None:
            if n is None:
                return df[column].sample()  # All sample outputs here only provide samples of the user-specified column
            else:
                return df[column].sample(n=n)
        elif n is None:
            return df[column].sample(frac=percent)
        else:
            return df


def stratified_sample(df: pd.DataFrame, column: str, codebook: pd.DataFrame,
                      n: int = None, percent: float = None) -> pd.DataFrame:
    # transforming fraction to number of data points if necessary
    if not n:
        n = round(percent * len(df))

    '''
    Temporary solution until more data on mixed is received as we have no data on each "bucket" of multiracial
    Easier to just bucket them together in the meantime until further data is received
    '''
    if column == "Q23":
        df.loc[df['Q23'].str.contains(','), 'Q23'] = 'Multiracial'

    # empty list to store dfSlices
    dfSlices = []

    # breaks up slices by column parameter, stores them in empty list
    for df_region in df.groupby(by=[column]).__iter__():
        if df_region[1][column].iloc[0] != "":
            dfSlices.append(df_region)

    # determines where to search for the percentages for each bucket
    size = eval(codebook['Distribution'].loc[codebook['Question ID'] == column].to_list()[0])  # TODO: remove eval
    # Todo: Try json.loads(...)?

    # creates list of the buckets
    try:
        slices = [random_sample(dfSlice[1], n=round(n * size[dfSlice[1][column].iloc[0]])) for dfSlice in
                  dfSlices]

    #if it needs more data points from a bucket than there actually are
    except KeyError as e:
        print("Key(s) " + str(e.args) + " not found in demographics.")
        return pd.DataFrame()
    except ValueError as e:
        print("Not enough data points in column " + str(column) + " to perform stratified sampling.")
        return pd.DataFrame()
    except NameError:
        print("No demographics for " + str(column))
        return pd.DataFrame()
    #sticks them together, returns
    return pd.concat(slices)


def weighted_sample(df: pd.DataFrame, column: str, n: int = None,
                    percent: float = None, weights: dict = None) -> pd.DataFrame:
    if not n and not percent:
        return pd.DataFrame()
    # transforming fraction to number of data points if necessary
    if not n:
        n = round(percent * len(df))

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
