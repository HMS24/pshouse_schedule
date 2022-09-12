from datetime import datetime


HEADERS = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,zh-CN;q=0.5",
    "Connection": "keep-alive",
    "DNT": "1",
    "sec-ch-ua": '" Not;A Brand";v="99", "Microsoft Edge";v="103", "Chromium";v="103"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "macOS",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36 Edg/103.0.1264.37",
    "X-Requested-With": "XMLHttpRequest",
}

zh_en_map = {
    "縣市": "city",
    "鄉鎮市區": "district",
    "交易標的": "object_of_transaction",
    "土地位置建物門牌": "location",
    "土地移轉總面積平方公尺": "land_total_area",
    "交易年月日": "transaction_date",
    "移轉層次": "level",
    "總樓層數": "total_floor_numbers",
    "建物型態": "building_state",
    "主要用途": "main_use",
    "建物移轉總面積平方公尺": "building_total_area",
    "建物現況格局-房": "room",
    "建物現況格局-廳": "restaurant_and_living_room",
    "建物現況格局-衛": "bathroom",
    "總價元": "price",
    "單價元平方公尺": "unit_price",
    "車位類別": "parking_sapce_type",
    "車位移轉總面積平方公尺": "parking_sapce_total_area",
    "車位總價元": "parking_sapce_price",
    "備註": "note",
    "建案名稱": "build_name",
    "棟及號": "buildings",
}

en_zh_map = {value: key for key, value in zh_en_map.items()}


def translate_column_names(columns, mapper):
    return [mapper.get(col, col) for col in columns]


def roc_to_ad_date(date_str):
    roc_year = date_str[:3]
    date_str = str(int(roc_year) + 1911) + date_str[3:]

    return datetime.strptime(date_str, "%Y%m%d")


def generate_saved_filename():
    today = datetime.now()
    day = _calculate_publish_day(today.day)

    date_str = today.strftime("%Y%m%d")
    publish_date_str = date_str[:6] + str(day)

    return f"{publish_date_str}_F_lvr_land_B.csv"


def _calculate_publish_day(day):
    # edge case
    if day == 21:
        return 21
    return (day // 11) * 10 + 1
