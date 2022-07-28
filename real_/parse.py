import logging
from datetime import datetime

from pydantic import ValidationError

from real_.models import RealEstateInfo
from real_.utils import mapping

logger = logging.getLogger()


def _translate_column_names(columns, mapper):
    return [mapper[col] for col in columns]


def _convert_roc_to_ad_date(date_str):
    roc_year = date_str[:3]
    date_str = str(int(roc_year) + 1911) + date_str[3:]

    return datetime.strptime(date_str, "%Y%m%d")


def parse_real_estate_info(df):
    logger.info("step: parse_real_estate_info")

    df = df.copy()

    # get needed columns
    columns = list(set(df.columns).intersection(set(mapping.zh_en_map)))
    df = df[columns]

    # translate columns name
    df.columns = _translate_column_names(df.columns, mapping.zh_en_map)

    # remove english description row(usually second row)
    en_column_name_index = df[df["main_use"] == "main use"].index
    df = df.drop(en_column_name_index)

    # parse ROC date
    df["transaction_date"] = (
        df["transaction_date"]
        .apply(_convert_roc_to_ad_date)
    )

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
    try:
        # why not use comprehension? because easily debug when using row
        results = []
        for row in df.to_dict("records"):
            results.append(RealEstateInfo(**row).dict())

        return results
    except ValidationError as e:
        logger.warning(
            f"real estate parse failed: {repr(e)}    ",
            f"district: {row['district']}, ",
            f"transaction_date: {row['transaction_date']}, ",
            f"build_name: {row['build_name']}, ",
            f"buildings: {row['buildings']}, ",
        )
