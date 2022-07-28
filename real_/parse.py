import csv
import logging
from io import StringIO
from datetime import datetime

import pandas as pd
from pydantic import ValidationError

from real_.models import ActualPriceRegistrationInfo
from real_.utils import mapping

logger = logging.getLogger()


def _translate_column_names(columns, mapper):
    return [mapper[col] for col in columns]


def _roc_to_ad_date(date_str):
    roc_year = date_str[:3]
    date_str = str(int(roc_year) + 1911) + date_str[3:]

    return datetime.strptime(date_str, "%Y%m%d")


def parse_actual_price_registration(content):
    logger.info("   step: parse_actual_price_registration")

    # encoding "utf-8-sig" for escaping UTF16_BOM
    # quoting "csv.QUOTE_NONE" 欄位會有誤輸入 quote 的時候
    df = pd.read_csv(
        StringIO(content),
        encoding="utf-8-sig",
        quoting=csv.QUOTE_NONE,
    )

    # get needed columns
    columns = list(set(df.columns).intersection(set(mapping.zh_en_map)))
    df = df[columns]

    # translate columns name
    df.columns = _translate_column_names(df.columns, mapping.zh_en_map)

    # remove english description row(usually second row)
    en_row_index = df[df["main_use"] == "main use"].index
    df = df.drop(en_row_index)

    # parse ROC date
    df["transaction_date"] = df["transaction_date"].apply(_roc_to_ad_date)

    # fill NaN
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

    # cast type
    results = []
    need_checked = []
    for record in df.to_dict("records"):
        try:
            results.append(ActualPriceRegistrationInfo(**record).dict())
        except ValidationError as e:
            logger.warning("    parse actual price registration failed")

            record['error_message'] = repr(e)
            need_checked.append(record)

    return results, need_checked
