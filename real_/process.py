import sys
import logging
from pathlib import Path

from real_ import config
from real_.fetch import fetch_real_estate
from real_.storage import save_to_storage

logger = logging.getLogger()


def process_real_estate():
    logger.info('step: process_real_estate')

    year, season = sys.argv[1:3]
    resp = fetch_real_estate(year, season)

    if not resp:
        return

    save_to_storage(
        dir_name=f'{year}S{season}',
        filepath=Path(config.STORAGE_ROOT_DIR).joinpath('F_lvr_land_B.csv'),
        content=resp.text
    )

    # parse
    # load into database
