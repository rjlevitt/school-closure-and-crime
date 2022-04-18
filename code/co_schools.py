import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt


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
    districts = districts.iloc[:, ::-1]
    plt.clf()
    plt.close()
    plot_dims = (6, 28)
    fig, ax = plt.subplots(figsize=plot_dims)

    cmap = plt.get_cmap('Blues', 3)
    ax = sns.heatmap(districts, cmap=cmap, vmin=1, vmax=3, square=True, cbar=False, linecolor='black')
    ax.set_xlabel(xlabel="")
    ax.set_ylabel(ylabel="District")

    # save
    cwd = os.path.abspath(os.path.dirname(__file__))

    fig.tight_layout()
    plt.savefig(os.path.join(cwd, "CO_teaching_methods_over_time.png"))


if __name__ == '__main__':
    schools, districts = read_data(data_path=get_data_path())
    heat_map(districts)
