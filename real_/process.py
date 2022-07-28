import sys
import logging
import csv
from io import StringIO
from pathlib import Path

import pandas as pd

from real_ import config
from real_.fetch import fetch_real_estate
from real_.storage import save_to_storage
from real_.parse import parse_real_estate_info
from real_.load import load_into_database

logger = logging.getLogger()


def process_real_estate():
    logger.info("start process_real_estate")

    year, season = sys.argv[1:3]
    content = fetch_real_estate(year, season)

    if content is None:
        return

    save_to_storage(
        dir_name=f"{year}S{season}",
        filepath=Path(config.STORAGE_ROOT_DIR).joinpath("F_lvr_land_B.csv"),
        content=content
    )

    # encoding "utf-8-sig" for escaping UTF16_BOM
    # quoting "csv.QUOTE_NONE" 欄位會有誤輸入 quote 的時候
    df = pd.read_csv(
        StringIO(content),
        encoding="utf-8-sig",
        quoting=csv.QUOTE_NONE
    )
    real_estate_info = parse_real_estate_info(df)

    load_into_database(real_estate_info)
