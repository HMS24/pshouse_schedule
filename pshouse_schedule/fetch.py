import os
import logging
from pathlib import Path
from datetime import datetime

import requests
from pyquery import PyQuery as pq

import pshouse_schedule.utils as utils
import pshouse_schedule.config as config
from pshouse_schedule.exceptions import NotUpdatedException

logger = logging.getLogger()


def fetch_deals():
    logger.info("   step: fetch_deals")

    params = {
        "fileName": "f_lvr_land_b.csv",
    }

    try:
        if is_resource_updated() == False:
            raise NotUpdatedException("resources haven't been updated yet")

        resp = requests.get(
            url="https://plvr.land.moi.gov.tw//Download",
            params=params,
            headers=utils.HEADERS,
        )

        # 當找不到該季或不正確的 fileName 時，會回傳 "系統發生錯誤，請洽系統管理人員" 的 html
        # 假設內政部的錯誤網頁不太會變動，判斷 Content-Length 較快，
        if int(resp.headers["Content-Length"]) == 541:
            raise Exception(
                f"https://plvr.land.moi.gov.tw server error")

        return resp.content
    except Exception as e:
        logger.warning(f"   fetch error: {repr(e)}")

        return None


def is_resource_updated():
    HISTORY_LIST_URL = "http://plvr.land.moi.gov.tw/DownloadHistory_ajax_list"

    history_page = requests.get(HISTORY_LIST_URL)
    doc = pq(history_page.text)

    offical_last_updated_date = (doc("table").eq(0)
                                 .children().eq(6)
                                 .children().eq(1)
                                 .text().strip().split(" ")[1])
    my_updated_list = [file[:8]
                    for file in os.listdir(config.STORAGE_ROOT_DIR)
                    if Path(file).suffix == ".csv"]
    if not my_updated_list:
        return True

    my_updated_list.sort(key=lambda date: datetime.strptime(date, "%Y%m%d"),
                      reverse=True)
    my_last_updated_date = my_updated_list[0]

    return offical_last_updated_date == my_last_updated_date
