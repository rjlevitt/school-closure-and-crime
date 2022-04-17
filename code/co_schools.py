import pandas as pd
import os


def get_data_path():
    cwd = os.path.abspath(os.path.dirname(__file__))
    data_path = os.path.join(cwd, 'rawdata')
    return data_path


def read_data(data_path):
    df = pd.read_csv(os.path.join(data_path, 'Colorado_Schools_LearningModelData_Final.csv'))
    return df


if __name__ == '__main__':
    dat = read_data(data_path=get_data_path())
    dat