import logging
import datetime

import requests
import pshouse_schedule.utils as utils

logger = logging.getLogger()


def fetch_deals():
    logger.info("   step: fetch_deals")

    params = {
        "fileName": "f_lvr_land_b.csv",
    }

    try:
        resp = requests.get(
            url="https://plvr.land.moi.gov.tw//Download",
            params=params,
            headers=utils.HEADERS,
        )

        # 當找不到該季或不正確的 fileName 時，會回傳 "系統發生錯誤，請洽系統管理人員" 的 html
        # 假設內政部的錯誤網頁不太會變動，判斷 Content-Length 較快，
        if int(resp.headers["Content-Length"]) == 541:
            today = str(datetime.datetime.now().date())
            raise Exception(
                f"current date {today} dataset has not been updated")

        return resp.content
    except Exception as e:
        logger.warning(f"   fetch error: {repr(e)}")

        return None
