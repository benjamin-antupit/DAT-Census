import pandas as pd
import os

from sample_methods import random_sample, stratified_sample, weighted_sample


def createAllOutputs(data_frame_list: list, output_dir):
    for title, df, header_labels in data_frame_list:
        if not df.empty:
            df.columns = [df.columns, list(header_labels)]  # Add questions as secondary headers
            df.dropna(how="all", inplace=True)  # Remove empty rows
            if not os.path.isdir('./'+output_dir):  # Create output directory if none exists
                os.mkdir('./'+output_dir)
            df.to_csv(output_dir + "/" + title + ".csv", index=False)  # Create CSVs


def parseData(file_name: str) -> ():
    data = pd.read_csv(file_name, header=0)  # Read CSV, create headers from first row
    data.drop(columns=['Status', 'Progress', 'RecordedDate', 'DistributionChannel', 'UserLanguage', "Finished",
                       "Q16 - Parent Topics", "Q16 - Topics"],
              axis=1, inplace=True, errors='ignore')  # Remove redundant columns
    header_labels = data.iloc[0]  # Save question names for later
    data.drop(index=0, inplace=True)  # Remove question names to avoid sampling errors
    data.fillna("", inplace=True)  # Fill all null values with empty string
    return data, header_labels


def parseCodebook(codebook_name: str) -> pd.DataFrame:
    codebook = pd.read_csv(codebook_name, header=0)
    codebook.dropna(inplace=True,
                    subset=['Question ID', 'OptionsProvided', 'QuestionType'])  # Remove empty rows
    codebook['OptionsProvided'] = codebook['OptionsProvided'].astype(bool)  # Convert string to bool
    return codebook


def getMultipleChoice(df: pd.DataFrame, headers, codebook: pd.DataFrame):
    headers = headers.copy()
    # Remove free response questions
    for i in range(2):
        (headers, df)[i].drop(list(codebook.loc[~codebook['OptionsProvided']]['Question ID']), inplace=True, axis=i)
    return df, headers


def getFreeTextResponse(df: pd.DataFrame, headers, codebook: pd.DataFrame):
    headers = headers.copy()
    # Remove multiple choice questions
    for i in range(2):
        (headers, df)[i].drop(list(codebook.loc[codebook['OptionsProvided']]['Question ID']), inplace=True, axis=i)
    return df, headers


def main(config, file_name=None, codebook_name=None, output_dir="output"):
    print("\nDAT Census Parsing & Sampling\n")

    if "US" in config:
        config = {'race_col': 'Q23', 'gender_col': 'Q20','grade_col': 'Q19', 'parent_edu_col': 'Q25'}
    elif "MS" in config:
        config = {'race_col': 'Q23', 'gender_col': 'Q20_1','grade_col': 'Q19', 'parent_edu_col': 'Q25'}
    elif "preliminary_US" in config:
        config = {'race_col': 'Q19', 'gender_col': 'Q17','grade_col': 'Q18', 'parent_edu_col': 'Q20'}
    elif "preliminary_MS" in config:
        config = {'race_col': 'Q20', 'gender_col': 'Q18','grade_col': 'Q19', 'parent_edu_col': 'Q21'}
    elif "mock" in config:
        config = {'race_col': 'Q24', 'gender_col': 'Q22','grade_col': 'Q23', 'parent_edu_col': 'Q25'}

    if not file_name:
        file_name = input("Please input name of results CSV: ")

    if not codebook_name:
        codebook_name = input("Please input name of codebook CSV: ")

    data, header_labels = parseData(file_name)
    codebook = parseCodebook(codebook_name)

    outputs = []
    print("Select one or more example output options:")
    print("0 - Create all options")
    print("1 - Parsed data (All question types)")
    print("2 - Parsed data (multiple choice only)")
    print("3 - Parsed data (free response only)")
    print("4 - Parse & sample data (Simple Random Sample)")
    print("5 - Parse & sample data (Stratified Sampling by race)")
    print("6 - Parse & sample data (Stratified Sampling by gender)")
    print("7 - Parse & sample data (Stratified Sampling by grade)")
    print("8 - Parse & sample data (Weighted Sampling by highest parental education)")
    options = input("Type one or more numbers to create selected outputs: ")

    if any(item in list(options) for item in ["0","4","5","6","7","8"]):
        n = input("How many responses should be returned (use __% to return percent of total responses): ")
        if "%" in n:
            n = round(float(n.strip("%")) / 100 * len(data.index))
        else:
            n = int(n)
        if n > len(data.index):
            n = len(data.index)

    if "1" in options or "0" in options:
        outputs.append(
            ("1_Parsed", data.copy(), header_labels))

    if "2" in options or "0" in options:
        outputs.append(
            ("2_Parsed_Multiple_Choice", *getMultipleChoice(data.copy(), header_labels, codebook)))

    if "3" in options or "0" in options:
        outputs.append(
            ("3_Parsed_Free_Response", *getFreeTextResponse(data.copy(), header_labels, codebook)))

    if "4" in options or "0" in options:
        outputs.append(
            ("4_Simple_Random_Sample_Parsed", random_sample(data.copy(), n=n), header_labels))

    if "5" in options or "0" in options:
        outputs.append(
            ("5_Stratified_Race_Parsed",
             stratified_sample(data.copy(), config['race_col'], codebook, n=n), header_labels))

    if "6" in options or "0" in options:
        outputs.append(
            ("6_Stratified_Gender_Parsed",
             stratified_sample(data.copy(), config['gender_col'], codebook, n=n), header_labels))

    if "7" in options or "0" in options:
        outputs.append(
            ("7_Stratified_Grade_Parsed",
             stratified_sample(data.copy(), config['grade_col'], codebook, n=n), header_labels))

    if "8" in options or "0" in options:
        outputs.append(
            ("8_Weighted_Education_Parsed",
             weighted_sample(data.copy(), config['parent_edu_col'], n=n), header_labels))

    createAllOutputs(outputs, output_dir)  # Create output CSVs with proper headers


# main("US", "input/CrystalCensusFinalUS_February 23, 2021_11.51.csv",
#      "input/Crystal_Census_Codebook_US.csv", "final_output_us")

main("MS", "input/CrystalCensusFinalMS_February 23, 2021_11.50.csv",
     "input/Crystal_Census_Codebook_MS.csv", "final_output_ms")
