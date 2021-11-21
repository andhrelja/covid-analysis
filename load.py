import os
import pandas as pd

from config import STAGE_PATH
from config import TARGET_PATH
from config import FOLDER_NAME
from config import OWID_FILE_NAME
from extract import validate_file_path

GROUPED_OWID_FILE_NAME = 'grouped-' + OWID_FILE_NAME
CROATIA_OWID_FILE_NAME = 'croatia-' + OWID_FILE_NAME

def load():
    validate_file_path(TARGET_PATH, FOLDER_NAME)
    stage_owid_path = os.path.join(STAGE_PATH, FOLDER_NAME, CROATIA_OWID_FILE_NAME)
    stage_grouped_owid_path = os.path.join(STAGE_PATH, FOLDER_NAME, GROUPED_OWID_FILE_NAME)

    target_owid_path = os.path.join(TARGET_PATH, FOLDER_NAME, CROATIA_OWID_FILE_NAME)
    target_grouped_owid_path = os.path.join(TARGET_PATH, FOLDER_NAME, GROUPED_OWID_FILE_NAME)
    
    df = pd.read_csv(stage_owid_path)
    df.to_csv(target_owid_path, index=False)

    grouped_df = pd.read_csv(stage_grouped_owid_path)
    grouped_df.to_csv(target_grouped_owid_path, index=False)


if __name__ == '__main__':
    load()