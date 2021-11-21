import os
import pandas as pd
import datetime as dt
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler

from config import INBOUND_PATH
from config import FOLDER_NAME
from config import OWID_FILE_NAME
from extract import validate_file_path

OWID_COLUMNS = [
    'iso_code', 'continent', 'location', 'date',
    'total_cases', 'new_cases', 'new_cases_smoothed',
    'total_deaths', 'new_deaths', 'new_deaths_smoothed',
    'reproduction_rate', 'positive_rate',
    'hosp_patients', 'hosp_patients_per_million',
    'weekly_icu_admissions', 'weekly_hosp_admissions',
    'total_vaccinations', 'people_vaccinated', 'people_fully_vaccinated',
    'new_vaccinations', 'new_vaccinations_smoothed',
    'population', 'population_density',
    'gdp_per_capita', 'extreme_poverty',
    'life_expectancy', 'human_development_index',

    'new_cases_smoothed_per_million', 'new_deaths_smoothed_per_million',
    'icu_patients_per_million', 'hosp_patients_per_million',
    'people_fully_vaccinated_per_hundred', 'new_vaccinations_smoothed_per_million',
    'stringency_index', 'median_age', 'excess_mortality'
]

INTERPOLATE_COLUMNS = [
    'total_vaccinations', 
    'people_vaccinated', 
    'people_fully_vaccinated'
]

NORMALIZE_COLUMNS = [
    'new_cases_smoothed',
    'new_deaths_smoothed',
    'total_deaths',
    'total_cases',
    'people_vaccinated_interpolated', 
    'people_fully_vaccinated_interpolated',
    'hosp_patients'
]

STANDARDIZE_COLUMNS = [
    'new_cases_smoothed',
    'new_deaths_smoothed',
    'people_vaccinated_interpolated', 
    'people_fully_vaccinated_interpolated',
    'hosp_patients'
]

def interpolate_columns(df):
    df = df.set_index('date', drop=False)
    for col in INTERPOLATE_COLUMNS:
        new_col = col + '_interpolated'
        df[new_col] = df.loc[dt.datetime(2021, 1, 1, 0, 0):dt.datetime.now(), col].interpolate()
    return df

def normalize_columns(df):
    for col in NORMALIZE_COLUMNS:
        new_col = col + '_normalized'
        df[new_col] = MinMaxScaler().fit_transform(df[col].values.reshape(-1, 1))
    return df

def standardize_columns(df):
    for col in STANDARDIZE_COLUMNS:
        new_col = col + '_standardized'
        df[new_col] = StandardScaler().fit_transform(df[col].values.reshape(-1, 1))
    return df

def get_owid_df():
    inbound_owid_path = os.path.join(
        INBOUND_PATH, 
        FOLDER_NAME, 
        OWID_FILE_NAME
    )
    df = pd.read_csv(inbound_owid_path)
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
    return df[OWID_COLUMNS]

def get_filtered_owid_df(filter_name, filter_value, df=None):
    if df is None:
        df = get_owid_df()
    
    if '_lte' in filter_name:
        filter_name = filter_name.replace('_lte', '')
        df = df[df[filter_name] <= filter_value]
    elif '_gte' in filter_name:
        filter_name = filter_name.replace('_gte', '')
        df = df[df[filter_name] >= filter_value]
    else:
        df = df[df[filter_name] == filter_value]
    df = interpolate_columns(df)
    df = normalize_columns(df)
    df = standardize_columns(df)
    return df

def get_positivity_rates_df(df):
    static_columns = [
        'location',
        'gdp_per_capita',
        'extreme_poverty',
        'life_expectancy',
        'human_development_index',
        'population',
        'population_density',
        'median_age',
    ]
    aggregate_columns = [
        'new_cases_smoothed_per_million',
        'new_deaths_smoothed_per_million',
        'icu_patients_per_million',
        'hosp_patients_per_million',
        'people_fully_vaccinated_per_hundred',
        'new_vaccinations_smoothed_per_million',
        'stringency_index',
        'excess_mortality'
    ]

    two_weeks_ago = dt.datetime.now() - dt.timedelta(days=15)
    df = df[df['date'] > two_weeks_ago]
    df = df[static_columns + aggregate_columns]
    for col in aggregate_columns:
        new_col = col + '_normalized'
        df[new_col] = MinMaxScaler().fit_transform(df[col].values.reshape(-1, 1))
    return df.groupby(static_columns).mean()


def write_target_owid(target_path):
    target_owid_path = os.path.join(
        target_path, 
        FOLDER_NAME,
        OWID_FILE_NAME
    )

    target_filtered_grouped_owid_path = os.path.join(
        target_path, 
        FOLDER_NAME,
        'grouped-' + OWID_FILE_NAME
    )
    
    target_df = get_owid_df()
    target_df.to_csv(target_owid_path)
    grouped_df = get_positivity_rates_df(target_df)
    grouped_df.to_csv(target_filtered_grouped_owid_path)


def write_target_filtered_owid(target_path, **filters):
    target_df = None
    target_filtered_owid_path = os.path.join(
        target_path, 
        FOLDER_NAME,
        '{}-'.format('croatia') + OWID_FILE_NAME
    )

    for key, item in filters.items():
        if target_df is None:
            target_df = get_filtered_owid_df(key, item)
        else:
            target_df = get_filtered_owid_df(key, item, target_df)
    target_df.to_csv(target_filtered_owid_path)

def transform_owid(target_path):
    validate_file_path(target_path, FOLDER_NAME)
    write_target_owid(target_path)
    write_target_filtered_owid(target_path, location='Croatia', date_gte='2021-01-01')

if __name__ == '__main__':
    transform_owid('./data/stage/')
    