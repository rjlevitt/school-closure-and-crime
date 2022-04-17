import pandas as pd
import os


def get_data_path():
    cwd = os.path.abspath(os.path.dirname(__file__))
    data_path = os.path.join(cwd, 'rawdata')
    return data_path


def prep_offense(data_path):
    offense = pd.read_csv(os.path.join(data_path, 'NIBRS_OFFENSE.csv'))
    offense_type = pd.read_csv(os.path.join(data_path, 'NIBRS_OFFENSE_TYPE.csv'))
    location = pd.read_csv(os.path.join(data_path, 'NIBRS_LOCATION_TYPE.csv'))
    df = offense.merge(offense_type, how="left", on=['OFFENSE_TYPE_ID'])
    df = df.merge(location, how="left", on=['LOCATION_ID'])
    df = df[[
        'DATA_YEAR',
        'OFFENSE_ID',
        'INCIDENT_ID',
        'OFFENSE_NAME',
        'CRIME_AGAINST',
        'OFFENSE_CATEGORY_NAME',
        'LOCATION_NAME']]
    return df


def prep_offenders(data_path):
    offender = pd.read_csv(os.path.join(data_path, 'NIBRS_OFFENDER.csv'))
    age = pd.read_csv(os.path.join(data_path, 'NIBRS_AGE.csv'))
    df = offender.merge(age, how="left", on="AGE_ID")
    df = df[[
        'DATA_YEAR',
        'OFFENDER_ID',
        'INCIDENT_ID',
        'AGE_NAME',
        'AGE_NUM',
        'AGE_RANGE_LOW_NUM',
        'AGE_RANGE_HIGH_NUM',
        'SEX_CODE'
    ]]
    return df


def prep_incident(data_path):
    incident = pd.read_csv(os.path.join(data_path, 'NIBRS_incident.csv'))
    agency = pd.read_csv(os.path.join(data_path, 'agencies.csv'))
    df = incident.merge(agency, how='inner', on=['AGENCY_ID', 'DATA_YEAR'])
    df = df[[
        'DATA_YEAR',
        'AGENCY_ID',
        'INCIDENT_ID',
        'NIBRS_MONTH_ID',
        'SUBMISSION_DATE',
        'INCIDENT_DATE',
        'INCIDENT_HOUR',
        'CLEARED_EXCEPT_ID',
        'CLEARED_EXCEPT_DATE',
        'ORI',
        'LEGACY_ORI',
        'REPORTING_TYPE',
        'UCR_AGENCY_NAME',
        'STATE_ABBR',
        'AGENCY_TYPE_NAME',
        'POPULATION',
        'POPULATION_GROUP_DESC',
        'COVERED_FLAG',
        'COUNTY_NAME']]
    return df


if __name__ == '__main__':
    dat_offense = prep_offense(data_path=get_data_path())
    dat_offender = prep_offenders(data_path=get_data_path())
    dat_incident = prep_incident(data_path=get_data_path())

    dat = dat_incident.merge(dat_offense, how="inner", on=['DATA_YEAR', 'INCIDENT_ID'])
    dat = dat.merge(dat_offender, how="inner", on=['DATA_YEAR', 'INCIDENT_ID'])
    dat.to_csv("~/Desktop/nibrs_co_2020.csv", index=False)
