import io
import logging
import csv

import pandas as pd
from pydantic import ValidationError

from pshouse_schedule.utils import (
    zh_en_map,
    en_zh_map,

    translate_column_names,
    roc_to_ad_date,
)
from pshouse_schedule.schemas import Deal

logger = logging.getLogger()


def parse_deals_info(raw):
    logger.info("   step: parse_deals_info")

    # encoding "utf-8-sig" for escaping UTF16_BOM
    # quoting "csv.QUOTE_NONE" 欄位會有誤輸入 quote 的時候
    df = pd.read_csv(
        io.StringIO(raw),
        encoding="utf-8-sig",
        quoting=csv.QUOTE_NONE,
    )

    columns = list(set(df.columns).intersection(set(zh_en_map)))
    df = df[columns]
    df.columns = translate_column_names(df.columns, zh_en_map)

    # add column city from location partition
    city = df.tail(1)["location"].values[0][:3]
    df["city"] = city

    # remove english description row(usually second row)
    en_row_index = df[df["main_use"] == "main use"].index
    df = df.drop(en_row_index)

    df["transaction_date"] = df["transaction_date"].apply(roc_to_ad_date)

    for col in df.columns:
        if col in ["transaction_date"]:
            continue
        elif col in [
            "land_total_area",
            "building_total_area",
            "parking_sapce_total_area",
            "price",
            "unit_price",
            "parking_sapce_price",
        ]:
            df[col] = df[col].fillna(0)
        else:
            df[col] = df[col].fillna("")

    # type conversion
    results = []
    need_checked = []
    for record in df.to_dict("records"):
        try:
            results.append(Deal(**record).dict())
        except ValidationError as e:
            logger.warning("    parse deal info failed")

            record["error_message"] = repr(e)
            need_checked.append(record)

    return results, need_checked


def parse_incorrect_deals_info(records):
    logger.info("   step: parse_incorrect_deals_info")

    if not records:
        return

    df = pd.DataFrame(records)
    df["transaction_date"] = df["transaction_date"].astype(str)
    df.columns = translate_column_names(df.columns, en_zh_map)

    return df.to_dict("records")
