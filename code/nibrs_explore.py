import pandas as pd
import os


def get_data_path():
    cwd = os.path.abspath(os.path.dirname(__file__))
    data_path = os.path.join(cwd, 'rawdata')
    return data_path


def read_merge_nibrs(data_path):
    incident = pd.read_csv(os.path.join(data_path, 'NIBRS_incident.csv'))
    offender = pd.read_csv(os.path.join(data_path, 'NIBRS_OFFENDER.csv'))
    agency = pd.read_csv(os.path.join(data_path, 'agencies.csv'))
    df = incident.merge(offender, how='inner', on=['INCIDENT_ID', 'DATA_YEAR'])
    df = df.merge(agency, how='inner', on='AGENCY_ID')
    return df


if __name__ == '__main__':
    dat = read_merge_nibrs(data_path=get_data_path())
