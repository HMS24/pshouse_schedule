from pandas import Timestamp
from dataclasses import dataclass


@dataclass
class MockResponse:
    text: str = ""
    status_code: int = 200


def mock_request_deals(url, params, headers):
    with open("./tests/data/F_lvr_land_B.csv", "r") as f:
        return MockResponse(text=f.read())


def mock_request_deals_failed(url, params, headers,):
    text = """
        \r\n \r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n \r\n<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">\r\n\r\n<html>\r\n<head>\r\n<title>施工中..</title>\r\n</head>\r\n<body>\r\n\t<table Border=\'0\' width="380" height="200" border="0" cellpadding="0"\r\n\t\tcellspacing="0" valign="top" align="center" background="">\r\n\t\t<tr align=left>\r\n\t\t\t<td align="left">檔案不存在</td>\r\n\t\t</tr>\r\n\t\t<tr>\r\n\t\t\t<td align=right valign="bottom">\r\n\t\t\t\t<img border="0"\tsrc="images/404.png">\r\n\t\t\t</td>\r\n\t\t</tr>\r\n\t\t<tr height=50 align=center>\r\n\t\t\t<td colspan=2 align=center><font size=2 color="red">&nbsp;\r\n\t\t\t</td>\r\n\t\t</tr>\r\n\t</table>\r\n</body>\r\n</html>\r\n
    """
    return MockResponse(text=text, status_code=404)


def mock_request_history_deals_list(url):
    with open("./tests/data/history.html", "r", encoding="utf-8") as f:
        return MockResponse(text=f.read())


EXPECTED_DEALS = [
    {
        'district': '泰山區',
        'object_of_transaction': '',
        'location': '新北市泰山區坡雅路信華三街口',
        'transaction_date': Timestamp('2022-07-13 00:00:00'),
        'level': '十三層',
        'total_floor_numbers': '15',
        'main_use': '住家用',
        'building_state': '住宅大樓(11層含以上有電梯)',
        'room': '2',
        'restaurant_and_living_room': '2',
        'bathroom': '1',
        'land_total_area': 0.0,
        'building_total_area': 93.11,
        'parking_sapce_total_area': 28.21,
        'price': 12500000,
        'unit_price': 157165,
        'parking_sapce_type': '坡道平面',
        'parking_sapce_price': 2300000,
        'note': '',
        'build_name': '朗朗城心',
        'buildings': 'A棟10-13F號',
    },
    {
        'district': '土城區',
        'object_of_transaction': '房地(土地+建物)+車位',
        'location': '新北市土城區金城路二段',
        'transaction_date': Timestamp('2022-07-11 00:00:00'),
        'level': '十層',
        'total_floor_numbers': '13',
        'main_use': '住家用',
        'building_state': '住宅大樓(11層含以上有電梯)',
        'room': '1',
        'restaurant_and_living_room': '1',
        'bathroom': '1',
        'land_total_area': 11.78,
        'building_total_area': 104.36,
        'parking_sapce_total_area': 30.36,
        'price': 14910000,
        'unit_price': 166351,
        'parking_sapce_type': '坡道平面',
        'parking_sapce_price': 2600000,
        'note': '',
        'build_name': '有富富玉',
        'buildings': 'C棟1號',
    },
]

EXPECTED_NEED_CHECKED_DEALS = [
    {
        'location': '新北市五股區成泰路三段',
        'transaction_date': Timestamp('2022-07-11 00:00:00'),
        'district': '五股區',
        'object_of_transaction': '房地(土地+建物)+車位',
        'parking_sapce_price': '1650000',
        'parking_sapce_total_area': '28.64',
        'land_total_area': '16.62',
        'level': '五層',
        'bathroom': '1',
        'note': '',
        'building_total_area': '123.73',
        'parking_sapce_type': '坡道平面',
        'main_use': '住家用',
        'price': '12470000',
        'build_name': '佳陞景漾',
        'total_floor_numbers': '15',
        'building_state': '住宅大樓(11層含以上有電梯)',
        'buildings': 'A棟A5-5F號',
        'unit_price': '113787',
        'restaurant_and_living_room': '1',
        'room': '999',
        'error_message': "ValidationError(model='Deal', errors=[{'loc': ('room',), 'msg': 'There are too many rooms. 999 rooms?', 'type': 'assertion_error'}])",
    },
]

EXPECTED_NEED_CHECKED_DEALS_PARSED = [
    {
        '土地位置建物門牌': '新北市五股區成泰路三段',
        '交易年月日': '2022-07-11',
        '鄉鎮市區': '五股區',
        '交易標的': '房地(土地+建物)+車位',
        '車位總價元': '1650000',
        '車位移轉總面積平方公尺': '28.64',
        '土地移轉總面積平方公尺': '16.62',
        '移轉層次': '五層',
        '建物現況格局-衛': '1',
        '備註': '',
        '建物移轉總面積平方公尺': '123.73',
        '車位類別': '坡道平面',
        '主要用途': '住家用',
        '總價元': '12470000',
        '建案名稱': '佳陞景漾',
        '總樓層數': '15',
        '建物型態': '住宅大樓(11層含以上有電梯)',
        '棟及號': 'A棟A5-5F號',
        '單價元平方公尺': '113787',
        '建物現況格局-廳': '1',
        '建物現況格局-房': '999',
        'error_message': "ValidationError(model='Deal', errors=[{'loc': ('room',), 'msg': 'There are too many rooms. 999 rooms?', 'type': 'assertion_error'}])",
    },
]
