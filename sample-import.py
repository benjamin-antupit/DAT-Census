import pandas as pd
import numpy as np


def sample_import(file_name):
    data = pd.read_csv(file_name, header=[0, 1])
    print(data.head())
    print(data.describe())


sample_import("input/Census Data Generation Mock Survey_January 11, 2021_18.36 - Sheet1 (1).csv")
