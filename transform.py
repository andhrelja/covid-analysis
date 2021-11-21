import os
import pandas as pd
import matplotlib.pyplot as plt

from config import STAGE_PATH
from config import FOLDER_NAME
from config import OWID_FILE_NAME
from config import KORONAVIRUS_FILE_NAME

from transform_owid import transform_owid
from transform_koronavirus import transform_koronavirus

OWID_FILE_NAME = 'croatia-' + OWID_FILE_NAME
KORONAVIRUS_FILE_NAME = KORONAVIRUS_FILE_NAME.replace('.json', '.csv')
JOINT_FILE_NAME = 'koronavirus-owid-covid-data.csv'

def combine_owid_koronavirus():
    target_owid_path = os.path.join(STAGE_PATH, FOLDER_NAME, OWID_FILE_NAME)
    target_koronavirus_path = os.path.join(STAGE_PATH, FOLDER_NAME, KORONAVIRUS_FILE_NAME)
    target_joint_path = os.path.join(STAGE_PATH, FOLDER_NAME, JOINT_FILE_NAME)
    
    owid_df = pd.read_csv(target_owid_path)
    koronavirus_df = pd.read_csv(target_koronavirus_path)
    
    owid_df = owid_df.set_index('date')
    koronavirus_df = koronavirus_df.set_index('date')
    
    joint_df = owid_df.join(koronavirus_df, rsuffix='_koronavirus', sort=True)
    joint_df.to_csv(target_joint_path)

def plot_differences():
    columns_to_plot = {
        'total_vaccinations': 'total_vaccinations_koronavirus',
        'people_vaccinated': 'people_vaccinated_koronavirus',
        'people_fully_vaccinated': 'people_fully_vaccinated_koronavirus',
        #'hosp_patients': 'hosp_patients'
    }
    
    
    target_joint_path = os.path.join(STAGE_PATH, FOLDER_NAME, OWID_FILE_NAME)
    owid_df = pd.read_csv(target_joint_path)
    #owid_df = owid_df[owid_df['date'] > '2021-01-01']
    
    fig, ax = plt.subplots(len(columns_to_plot), sharex=True)
    for i, (owid_column, koronavirus_column) in enumerate(columns_to_plot.items()):
        ax[i].set_title(owid_column)
        ax[i].plot(owid_df['date'], owid_df[owid_column], 'r-', label=owid_column)
        
        interpolated_column = owid_column + "_interpolated"
        #owid_df[interpolated_column] = owid_df[owid_column].interpolate()
        ax[i].plot(owid_df['date'], owid_df[interpolated_column], 'b--', label=interpolated_column)
        #ax[i].plot(owid_df['date'], owid_df[koronavirus_column], 'b--', label=koronavirus_column)
        ax[i].legend()
    

def transform():
    transform_owid(STAGE_PATH)
    # transform_koronavirus(STAGE_PATH)
    # combine_owid_koronavirus()

if __name__ == '__main__':
    #transform()
    plot_differences()
    input()