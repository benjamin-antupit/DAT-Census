import pandas as pd

from random_sample import random_sample
from stratified_sample import stratified_sample
from weighted_sample import weighted_sample


def createAllOutputs(data_frame_list: list, header_labels):
    for title, df in data_frame_list:
        if not df.empty:
            df = pd.concat((df, header_labels), axis=1)
            df.drop(df.columns[-1], axis=1, inplace=True)
            df.dropna(how="all", inplace=True)
            df.to_csv("output/" + title + ".csv", index=False)


def parse(file_name: str) -> ():
    data = pd.read_csv(file_name, header=0)
    header_labels = data.iloc[0]
    # for index, column in data.iteritems():
    #   headers.append(column.values[0] + " (" + column.values[1] + ")")
    # data.columns = headers  # must be same length as columns

    # print(data.describe())

    data.drop(index=0, inplace=True)
    data.drop(columns=['Status', 'Progress', 'RecordedDate', 'DistributionChannel', 'UserLanguage', "Finished"],
              axis=1, inplace=True)
    # data.dropna(inplace=True)
    # print(data.columns)

    # TODO: fix double header row
    return data, header_labels


def getMultipleChoice(df: pd.DataFrame):
    return df


def getTextResponse(df: pd.DataFrame):
    return df


def main():
    print("\nDAT Census Parsing & Sampling\n")

    data, header_labels = parse("input/Mock Census Data - Sheet1.csv")  # parse(input("Please input name of CSV: "))

    outputs = []
    print("Select one or more example output options:")
    print("0 - Create all options")
    print("1 - Parsed data (All question types)")
    print("2 - Parsed data (multiple choice only)")
    print("3 - Parsed data (free response only)")
    print("4 - Parse data (Simple Random Sample)")
    print("5 - Parse data (Stratified Sampling by race)")
    print("6 - Parse data (Stratified Sampling by gender)")
    print("7 - Parse data (Weighted Sampling by highest parental education)")
    options = input("Type one or more numbers to create selected outputs: ")

    if "1" in options or "0" in options:
        # parsed only
        outputs.append(("Parsed", data.copy()))

    if "2" in options or "0" in options:
        # TODO mult choice only
        outputs.append(("Parsed_Multiple_Choice", data.copy()))

    if "3" in options or "0" in options:
        # TODO free response only
        outputs.append(("Parsed_Free_Response", data.copy()))

    if "4" in options or "0" in options:
        # simple random
        outputs.append(("Simple_Random_Sample_Parsed", random_sample(data.copy(), None, 0.5)))

    if "5" in options or "0" in options:
        # stratified by grade
        outputs.append(("Stratified_Race_Parsed", stratified_sample(data.copy(), "Q24",4)))

    if "6" in options or "0" in options:
        # stratified by how many people you live with
        outputs.append(("Stratified_Gender_Parsed", stratified_sample(data.copy(), "Q22",4)))

    if "7" in options or "0" in options:
        # weighted by parent education
        outputs.append(("Weighted_Education_Parsed", weighted_sample(data.copy(), "Q25", None)))

    createAllOutputs(outputs, header_labels)


main()

# parse("input/Mock Census Data - Sheet1.csv")
