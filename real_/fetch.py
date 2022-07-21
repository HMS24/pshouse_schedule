import logging

import requests
from real_.utils import constants

logger = logging.getLogger()


def fetch_real_estate(year, season) -> None:
    logger.info('step: fetch_real_estate')

    year = int(year)
    if year > 1000:
        year -= 1911

    params = {
        'season': f'{year}S{season}',
        'fileName': 'F_lvr_land_B.csv',
    }

    try:
        resp = requests.get(
            url='https://plvr.land.moi.gov.tw//DownloadSeason',
            params=params,
            headers=constants.HEADERS
        )

        if not resp.text.startswith(constants.UTF16_BOM):
            raise Exception(f'dataset {year}S{season} has not been updated')

        return resp.text
    except Exception as e:
        logger.warning(f'fetch error: {repr(e)}')

        return None
