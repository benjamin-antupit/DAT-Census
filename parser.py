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
    data.fillna("", inplace=True)
    return data, header_labels


def getMultipleChoice(df: pd.DataFrame):
    return df.drop(columns=["Q1_5_TEXT", "Q16", "Q18", "Q22_4_TEXT", "Q26_11_TEXT"])


def getFreeTextResponse(df: pd.DataFrame):
    return df.drop(columns=["Q1_1", "Q1_2", "Q1_3", "Q1_4", "Q1_5", "Q3", "Q4_1", "Q5", "Q6_1", "Q6_2", "Q6_3", "Q6_4",
                            "Q9_1", "Q9_2", "Q9_3", "Q9_4", "Q10_1", "Q12_1", "Q12_2", "Q12_3", "Q12_4", "Q12_5",
                            "Q12_6", "Q12_7", "Q13_1", "Q13_2", "Q14_1", "Q14_2", "Q14_3", "Q14_4", "Q15_1", "Q15_2",
                            "Q15_3", "Q15_4", "Q17", "Q19_1", "Q19_2", "Q19_3", "Q19_4", "Q19_5", "Q19_6", "Q19_7",
                            "Q21", "Q22", "Q23", "Q24", "Q25", "Q26", "Q27"])


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
        outputs.append(("1_Parsed", data.copy()))

    if "2" in options or "0" in options:
        # TODO mult choice only
        outputs.append(("2_Parsed_Multiple_Choice", getMultipleChoice(data.copy())))

    if "3" in options or "0" in options:
        # TODO free response only
        outputs.append(("3_Parsed_Free_Response", getFreeTextResponse(data.copy())))

    if "4" in options or "0" in options:
        # simple random
        outputs.append(("4_Simple_Random_Sample_Parsed", random_sample(data.copy(), None, 0.5)))

    if "5" in options or "0" in options:
        # stratified by grade
        outputs.append(("5_Stratified_Race_Parsed", stratified_sample(data.copy(), "Q24", fraction=0.25)))

    if "6" in options or "0" in options:
        # stratified by how many people you live with
        outputs.append(("6_Stratified_Gender_Parsed", stratified_sample(data.copy(), "Q22", fraction=0.5)))

    if "7" in options or "0" in options:
        # weighted by parent education
        outputs.append(("7_Weighted_Education_Parsed", weighted_sample(data.copy(), "Q25", frac=0.5)))

    createAllOutputs(outputs, header_labels)


main()

# parse("input/Mock Census Data - Sheet1.csv")
