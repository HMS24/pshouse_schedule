import logging
from datetime import datetime

from pydantic import BaseModel, ValidationError


logger = logging.getLogger()

zh_en_map = {
    '鄉鎮市區': 'district',
    '交易標的': 'object_of_transaction',
    '土地位置建物門牌': 'location',
    '土地移轉總面積平方公尺': 'land_total_area',
    '交易年月日': 'transaction_date',
    '移轉層次': 'level',
    '總樓層數': 'total_floor_numbers',
    '建物型態': 'building_state',
    '主要用途': 'main_use',
    '建物移轉總面積平方公尺': 'building_total_area',
    '建物現況格局-房': 'room',
    '建物現況格局-廳': 'restaurant_and_living_room',
    '建物現況格局-衛': 'bathroom',
    '總價元': 'price',
    '單價元平方公尺': 'unit_price',
    '車位類別': 'parking_sapce_type',
    '車位移轉總面積平方公尺': 'parking_sapce_total_area',
    '車位總價元': 'parking_sapce_price',
    '備註': 'note',
    '建案名稱': 'build_name',
    '棟及號': 'buildings',
}


class RealEstateInfo(BaseModel):
    district: str = ''
    object_of_transaction: str = ''
    location: str = ''
    transaction_date: datetime = None
    level: str = ''
    total_floor_numbers: str = ''
    main_use: str = ''
    building_state: str = ''
    room: str = ''
    restaurant_and_living_room: str = ''
    bathroom: str = ''
    land_total_area: float = 0.00
    building_total_area: float = 0.00
    parking_sapce_total_area: float = 0.00
    price: int = 0
    unit_price: int = 0
    parking_sapce_type: str = ''
    parking_sapce_price: int = 0
    note: str = ''
    build_name: str = ''
    buildings: str = ''


def translate_column_names(columns, mapper):
    return [mapper[col] for col in columns]


def convert_roc_to_ad_date(date_str):
    roc_year = date_str[:3]
    date_str = str(int(roc_year) + 1911) + date_str[3:]

    return datetime.strptime(date_str, '%Y%m%d')


def parse_real_estate_info(df):
    logger.info('step: parse_real_estate_info')

    df = df.copy()

    # get needed columns
    columns = list(set(df.columns).intersection(set(zh_en_map)))
    df = df[columns]

    # translate columns name
    df.columns = translate_column_names(df.columns, zh_en_map)

    # remove english description row(usually second row)
    en_column_name_index = df[df['main_use'] == 'main use'].index
    df = df.drop(en_column_name_index)

    # parse ROC date
    df['transaction_date'] = (
        df['transaction_date']
        .apply(convert_roc_to_ad_date)
    )

    # fill NaN
    for col in df.columns:
        if col in ['transaction_date']:
            continue
        elif col in [
            'land_total_area',
            'building_total_area',
            'parking_sapce_total_area',
            'price',
            'unit_price',
            'parking_sapce_price',
        ]:
            df[col] = df[col].fillna(0)
        else:
            df[col] = df[col].fillna('')

    # cast type
    try:
        # why not use comprehension? because easily debug when using row
        results = []
        for row in df.to_dict('records'):
            results.append(RealEstateInfo(**row).dict())

        return results
    except ValidationError as e:
        logger.warning(
            f'real estate parse failed: {repr(e)}    ',
            f'district: {row["district"]}, ',
            f'transaction_date: {row["transaction_date"]}, ',
            f'build_name: {row["build_name"]}, ',
            f'buildings: {row["buildings"]}, ',
        )
