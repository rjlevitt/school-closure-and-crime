import pandas as pd
import os


def get_data_path():
    cwd = os.path.abspath(os.path.dirname(__file__))
    data_path = os.path.join(cwd, 'rawdata')
    return data_path


def read_nibrs_data(data_path):
    incident = pd.read_csv(os.path.join(data_path, 'NIBRS_incident.csv'))
    offender = pd.read_csv(os.path.join(data_path, 'NIBRS_OFFENDER.csv'))
    return incident, offender


if __name__ == '__main__':
    incident, offender = read_nibrs_data(data_path=get_data_path())
    df = incident.merge(offender, how='inner', on=['INCIDENT_ID', 'DATA_YEAR'])
