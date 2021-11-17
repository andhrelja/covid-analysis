import datetime as dt
import os

BASE_DIR = 'C:\\Users\\AndreaHrelja\\Documents\\Faks\\5. godina\\3. semestar\\UPZ\\Seminar'

INBOUND_PATH = os.path.join(BASE_DIR, 'data\\inbound')
STAGE_PATH = os.path.join(BASE_DIR, 'data\\stage')
TARGET_PATH = os.path.join(BASE_DIR, 'data\\target')

FOLDER_NAME = str(dt.date.today())

OWID_FILE_NAME = 'owid-covid-data.csv'
KORONAVIRUS_FILE_NAME = 'koronavirus-covid-data.json'
