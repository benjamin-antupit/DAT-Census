import pandas as pd
import numpy as np


def sample_import(file_name):
    data = pd.read_csv(file_name, header=[0, 1])
    print(data.head())
    print(data.describe())


sample_import("input/Mock Census Data - Sheet1.csv")
