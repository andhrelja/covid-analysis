import datetime as dt
import os

BASE_DIR = os.path.dirname(__file__)

INBOUND_PATH = os.path.join(BASE_DIR, 'data\\inbound')
STAGE_PATH = os.path.join(BASE_DIR, 'data\\stage')
TARGET_PATH = os.path.join(BASE_DIR, 'data\\target')

FOLDER_NAME = str(dt.date.today())

OWID_FILE_NAME = 'owid-covid-data.csv'
KORONAVIRUS_FILE_NAME = 'koronavirus-covid-data.json'

if __name__ == '__main__':
    print(__file__)