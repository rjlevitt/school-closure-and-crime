import pandas as pd
import os
from matplotlib import pyplot as plt
import matplotlib as mpl


def get_data_path(year, local=False):
    cwd = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if(local):
        cwd = os.path.abspath(os.path.dirname(__file__))

    data_path = os.path.join(cwd, 'rawdata', str(year))
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


def hs_timeseries_offenses(df, var_name, var_title, color, plot_path):

    # copy datasets
    hs_dat = df[~df['AGE_NUM'].isna()].copy()

    # subset by age and crime type
    hs_dat = hs_dat[(hs_dat.AGE_NUM > 13) & (hs_dat.AGE_NUM < 19)]

    if var_name != 'total':
        hs_dat = hs_dat[hs_dat['CRIME_AGAINST'] == var_name]

    # year and month
    hs_dat['year'] = pd.to(hs_dat['INCIDENT_DATE']).year
    hs_dat['month'] = pd.DatetimeIndex(hs_dat['INCIDENT_DATE']).month

    # create a count variable and sum
    hs_dat["count"] = 1
    total_hs = hs_dat[['year', 'month', 'count']].groupby(
        ['year', 'month'], as_index=False).sum()

    # labels
    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug",
                   "Sep", "Oct", "Nov", "Dec"]

    # plot
    fig, ax = plt.subplots(figsize=(8, 4))
    plt.plot(total_hs['month'], total_hs['count'], color=color)
    ax.set_xticks(total_hs['month'])
    ax.set_xticklabels(month_names)
    ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
    for side in ['top', 'right', 'bottom', 'left']:
        ax.spines[side].set_visible(False)
    plt.ylabel("Count of Offenses")
    plt.grid(color='#f0f0f0')
    plt.title(var_title)
    plt.tight_layout()
    plt.savefig(plot_path)


def age_buckets(data):

    # drop missing age data
    df = data.copy()
    df = df[~df['AGE_NUM'].isna()]

    df['age_group'] = "None"

    df.loc[df['AGE_NUM'] < 5, 'age_group'] = "Less than 5"
    df.loc[(df['AGE_NUM'] >= 5) & (df['AGE_NUM'] < 11), 'age_group'] = "6 to 10"
    df.loc[(df['AGE_NUM'] >= 11) & (df['AGE_NUM'] < 16), 'age_group'] = "11 " \
                                                                        "to 15"
    df.loc[ (df['AGE_NUM'] >= 16) & (df['AGE_NUM'] < 21), 'age_group'] = "16 " \
                                                                         "to 20"
    df.loc[(df['AGE_NUM'] >= 21) & (df['AGE_NUM'] < 26), 'age_group'] = "21 " \
                                                                        "to 25"
    df.loc[(df['AGE_NUM'] >= 26) & (df['AGE_NUM'] < 31), 'age_group'] = "26 " \
                                                                        "to 30"
    df.loc[(df['AGE_NUM'] >= 31) & (df['AGE_NUM'] < 36), 'age_group'] = "30 " \
                                                                        "to 35"
    df.loc[(df['AGE_NUM'] >= 36) & (df['AGE_NUM'] < 41), 'age_group'] = "36 " \
                                                                        "to 40"
    df.loc[(df['AGE_NUM'] >= 41), 'age_group'] = "Greater than 40"

    return df


def full_year_prep(year):
    dat_offense = prep_offense(data_path=get_data_path(year=year))
    dat_offender = prep_offenders(data_path=get_data_path(year=year))
    dat_incident = prep_incident(data_path=get_data_path(year=year))

    dat = dat_incident.merge(dat_offense,
                             how="inner",
                             on=['DATA_YEAR', 'INCIDENT_ID'])

    dat = dat.merge(dat_offender,
                    how="inner",
                    on=['DATA_YEAR', 'INCIDENT_ID'])
    return dat


if __name__ == '__main__':
    dat_19 = full_year_prep(2019)
    dat_20 = full_year_prep(2020)

    # row bind two data sets
    dat = pd.concat([dat_19, dat_20])

    # create age buckets
    dat = age_buckets(dat)

    # add year and month based on indcident dat
    dat['year'] = pd.to_datetime(dat['INCIDENT_DATE']).dt.strftime('%Y')
    dat['month'] = pd.to_datetime(dat['INCIDENT_DATE']).dt.strftime('%m')

    # create a count of offenses
    dat["count"] = 1

    dat = dat[[
        'AGENCY_ID',
        'ORI',
        'COUNTY_NAME',
        'year',
        'month',
        'count',
        'CRIME_AGAINST',
        'age_group']]

    # sum offenses
    dat = dat.groupby(by=['AGENCY_ID',
                          'ORI',
                          'COUNTY_NAME',
                          'year',
                          'month',
                          'CRIME_AGAINST',
                          'age_group'], as_index=False)['count'].sum()

    cwd = os.path.abspath(os.path.dirname(__file__))
    dat = dat.rename(columns={
        'AGENCY_ID': 'agency_id',
        'ORI': 'ori',
        'COUNTY_NAME': 'county',
        'CRIME_AGAINST': 'crimes_against',
        'age_group': 'age_group'
    })
    
    dat.to_csv("final_crime_co.csv", index=False)
    # hs_timeseries_offenses(df=dat,
    #                        var_name='Person',
    #                        var_title=f"Offenses Against Persons in {year} by "
    #                                  f"HS "
    #                                  "Aged "
    #                                  "Offenders",
    #                        color='#e377c2',
    #                        plot_path=os.path.join(
    #                            cwd, 'plots', f'violent_offenses_{year-2000}.png'))

