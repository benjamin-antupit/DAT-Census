import pandas as pd

import random_sample
import stratified_sample
import weighted_sample


def createAllOutputs(data_frame_list: list):
    for i in range(len(data_frame_list)):
        if not data_frame_list[i].empty:
            data_frame_list[i].to_csv("output/" + str(i) + ".csv", index=False)


def parse(file_name: str) -> pd.DataFrame:
    data = pd.read_csv(file_name, header=[0, 1])
    # print(data.head())
    # print(data.describe())

    data.drop(columns=['Status', 'Progress', 'RecordedDate', 'DistributionChannel', 'UserLanguage'],
              inplace=True, level=1, errors='ignore')
    # data.dropna(inplace=True)
    # print(data.columns)

    # TODO: fix double header row
    return data


def getMultipleChoice(df: pd.DataFrame):
    return df


def getTextResponse(df: pd.DataFrame):
    return df


def main():
    print("DAT Census Parsing & Sampling\n")

    data = parse("input/Mock Census Data - Sheet1.csv")  # parse(input("Please input name of CSV: "))

    outputs = []
    print("Select one or more example output options:")
    print("0 - Create all options")
    print("1 - Parsed data (All question types)")
    print("2 - Parsed data (multiple choice only)")
    print("3 - Parsed data (free response only)")
    print("4 - Parse data (Simple Random Sample)")
    print("5 - Parse data (Stratified Sampling by grade)")
    print("6 - Parse data (Stratified Sampling by people in household)")
    print("7 - Parse data (Weighted Sampling by highest parental education)")
    options = input("Type one or more numbers to create selected outputs: ")

    if "1" in options or "0" in options:
        # parsed only
        outputs.append(data.copy())
    elif "2" in options or "0" in options:
        # TODO mult choice only
        outputs.append(data)
    elif "3" in options or "0" in options:
        # TODO free response only
        outputs.append(data)
    elif "4" in options or "0" in options:
        # simple random
        outputs.append(random_sample.random_sample(data.copy(), None, 0.5))
    elif "5" in options or "0" in options:
        # stratified by grade
        outputs.append(stratified_sample.stratified_sample(data.copy(), ["Q23"]))
    elif "6" in options or "0" in options:
        # stratified by how many people you live with
        outputs.append(stratified_sample.stratified_sample(data.copy(), "Q26"))
    elif "7" in options or "0" in options:
        # weighted by parent education
        outputs.append(weighted_sample.weighted_sample(data.copy(), "Q25", None))

    createAllOutputs(outputs)


main()

# parse("input/Mock Census Data - Sheet1.csv")
