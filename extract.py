import os
import requests

from config import INBOUND_PATH
from config import FOLDER_NAME
from config import OWID_FILE_NAME
from config import KORONAVIRUS_FILE_NAME

owid_data_url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'
koronavirus_data_url = 'https://www.koronavirus.hr/json/?action=podaci'

def download_owid_csv(file_name):
    response = requests.get(owid_data_url)

    file_path = os.path.join(INBOUND_PATH, FOLDER_NAME, file_name)
    with open(file_path, 'w') as f:
        f.write(response.text)

def download_koronavirus_json(file_name):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0'
    }
    response = requests.get(koronavirus_data_url, headers=headers)
    
    file_path = os.path.join(INBOUND_PATH, FOLDER_NAME, file_name)
    with open(file_path, 'w') as f:
        f.write(response.text)

def validate_file_path(path, folder_name):
    folder_path = os.path.join(path, folder_name)
    if not os.path.isdir(folder_path):
        os.mkdir(folder_path)

def extract():
    validate_file_path(INBOUND_PATH, FOLDER_NAME)
    download_owid_csv(file_name=OWID_FILE_NAME)
    download_koronavirus_json(file_name=KORONAVIRUS_FILE_NAME)

if __name__ == '__main__':
    extract()