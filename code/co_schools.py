import pandas as pd
import os
import numpy as np

def get_data_path():
    cwd = os.path.abspath(os.path.dirname(__file__))
    data_path = os.path.join(cwd, 'rawdata')
    return data_path


def read_data(data_path):
    schools = pd.read_csv(os.path.join(data_path, 'Colorado_Schools_LearningModelData_Final.csv'))
    districts = pd.read_csv(os.path.join(data_path, 'Colorado_Districts_LearningModelData_Final.csv'))
    return schools, districts


def school_closure_code(df):
    df["912_code"] = 1
    df.loc[df["LearningModelGr912"] == "Virtual", "912_code"] = 2
    df.loc[df["LearningModelGr912"] == "Hybrid", "912_code"] = 3
    df.loc[(df["LearningModelGr912"]).isnull(), "912_code"] = np.nan
    return df


def heat_map(districts):
    import seaborn as sns

    districts = school_closure_code(districts)
    districts = districts[[
        'DistrictName',
        'TimePeriodStart',
        '912_code']]
    districts = districts.pivot_table(index=['DistrictName'], columns='TimePeriodStart', values='912_code')

    cmap = plt.get_cmap('jet', 3)
    p1 = sns.heatmap(districts, cmap=cmap, vmin=1, vmax=3)
    plt.show()


if __name__ == '__main__':
    schools, districts = read_data(data_path=get_data_path())
