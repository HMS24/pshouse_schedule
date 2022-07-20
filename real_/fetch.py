import logging
from pathlib import Path

import requests

from real_.config import STORE_ROOT_DIR
from real_.utils import constants
from real_.utils.file import extract_to

logger = logging.getLogger()


def fetch_real_estate(year, season) -> None:
    year = int(year)
    if year > 1000:
        year -= 1911

    params = {
        'season': f'{year}S{season}',
        'type': 'zip',
        'fileName': 'lvr_landcsv.zip'
    }

    try:
        resp = requests.get(
            url='https://plvr.land.moi.gov.tw//DownloadSeason',
            params=params,
            headers=constants.HEADERS
        )
        extract_to(
            folderpath=Path(STORE_ROOT_DIR).joinpath(f'{year}-{season}'),
            content=resp.content,
        )
    except Exception as e:
        logger.warning(f'fetch error: {repr(e)}')
