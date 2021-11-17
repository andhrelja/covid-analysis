import os
import json
import pandas as pd

from extract import INBOUND_PATH
from extract import FOLDER_NAME
from extract import KORONAVIRUS_FILE_NAME
from extract import validate_file_path

KORONAVIRUS_COLUMNS = {
    'SlucajeviHrvatska': 'total_cases',
    'UmrliHrvatska': 'total_deaths',
    'CijepljenjeBrUtrosenihDoza': 'total_vaccinations',
    'CijepljeniJednomDozom': 'people_vaccinated',
    'CijepljeniDvijeDoze': 'people_fully_vaccinated',
    'Datum': 'date',
}

INBOUND_KORONAVIRUS_PATH = os.path.join(
    INBOUND_PATH, 
    FOLDER_NAME, 
    KORONAVIRUS_FILE_NAME
)

def _read_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def _write_json(content, file_path):
    with open(file_path, 'w') as f:
        return json.dump(content, f)

def _find_items(content, _date):
    for item in content:
        if item['Datum'] == _date:
            yield item

def get_koronavirus_df():
    df = pd.read_json(INBOUND_KORONAVIRUS_PATH)
    df = df.rename(columns=KORONAVIRUS_COLUMNS)
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d %H:%M')
    return df[KORONAVIRUS_COLUMNS.values()]

def write_resolved_duplicates_json():
    content = _read_json(INBOUND_KORONAVIRUS_PATH)
    uniques = []
    duplicates = []
    for item in content:
        if item['Datum'] not in uniques:
            uniques.append(item['Datum'])
        elif item['Datum'] in uniques:
            duplicates.append(item['Datum'])
    
    for item in content:
        if item['Datum'] in duplicates:
            for dup_item in _find_items(content, item['Datum']):
                if dup_item['SlucajeviHrvatska'] > item['SlucajeviHrvatska']:
                    item['Datum'] = '1970-01-01 00:00'
    _write_json(content, INBOUND_KORONAVIRUS_PATH)

def write_target_koronavirus(target_path):
    target_owid_path = os.path.join(
        target_path, 
        FOLDER_NAME,
        KORONAVIRUS_FILE_NAME.replace('.json', '.csv')
    )
    
    target_df = get_koronavirus_df()
    target_df.to_csv(target_owid_path, index=False)

def transform_koronavirus(target_path):
    validate_file_path(target_path, FOLDER_NAME)
    write_resolved_duplicates_json()
    write_target_koronavirus(target_path)

if __name__ == '__main__':
    transform_koronavirus('./data/stage/')
