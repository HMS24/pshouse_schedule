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

        # 當找不到該季或不正確的 fileName 時，會回傳 "系統發生錯誤，請洽系統管理人員" 的 html
        # 假設內政部的錯誤網頁不太會變動，判斷 Content-Length 比較快，
        if int(resp.headers['Content-Length']) == 541:
            raise Exception(f'dataset {year}S{season} has not been updated')

        return resp.text
    except Exception as e:
        logger.warning(f'fetch error: {repr(e)}')

        return None
