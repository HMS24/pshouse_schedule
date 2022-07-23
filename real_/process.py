import sys
import logging
from pathlib import Path

import pandas as pd

from real_ import config
from real_.fetch import fetch_real_estate
from real_.storage import save_to_storage
from real_.parse import parse_real_estate_info
from real_.load import load_into_database

logger = logging.getLogger()


def process_real_estate():
    logger.info('start process_real_estate')

    year, season = sys.argv[1:3]
    real_estate_content = fetch_real_estate(year, season)

    if real_estate_content is None:
        return

    # save as a local file then upload storage
    filepath = Path(config.STORAGE_ROOT_DIR).joinpath('F_lvr_land_B.csv')
    save_to_storage(
        dir_name=f'{year}S{season}',
        filepath=filepath,
        content=real_estate_content
    )

    # encoding 'utf-8-sig' for escaping UTF16_BOM
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        df = pd.read_csv(f)
        real_estate_info = parse_real_estate_info(df)

    load_into_database(real_estate_info)
