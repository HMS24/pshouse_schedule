from dataclasses import dataclass


@dataclass
class MockResponse:
    text: str = ""


def mock_request_deals(url, params, headers):
    with open("./tests/data/F_lvr_land_B.csv", "r") as f:
        return MockResponse(text=f.read())


def mock_request_deals_failed(url, params, headers,):
    text = """
        \r\n \r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n\r\n \r\n<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">\r\n\r\n<html>\r\n<head>\r\n<title>施工中..</title>\r\n</head>\r\n<body>\r\n\t<table Border=\'0\' width="380" height="200" border="0" cellpadding="0"\r\n\t\tcellspacing="0" valign="top" align="center" background="">\r\n\t\t<tr align=left>\r\n\t\t\t<td align="left">檔案不存在</td>\r\n\t\t</tr>\r\n\t\t<tr>\r\n\t\t\t<td align=right valign="bottom">\r\n\t\t\t\t<img border="0"\tsrc="images/404.png">\r\n\t\t\t</td>\r\n\t\t</tr>\r\n\t\t<tr height=50 align=center>\r\n\t\t\t<td colspan=2 align=center><font size=2 color="red">&nbsp;\r\n\t\t\t</td>\r\n\t\t</tr>\r\n\t</table>\r\n</body>\r\n</html>\r\n
    """
    return MockResponse(text=text)
