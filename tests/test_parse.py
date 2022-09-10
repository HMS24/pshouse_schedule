from pshouse_schedule.parse import (
    parse_deals_info,
    parse_incorrect_deals_info,
)
from tests.mock import (
    EXPECTED_DEALS,
    EXPECTED_NEED_CHECKED_DEALS,
    EXPECTED_NEED_CHECKED_DEALS_PARSED,
)


def test_parse_deals_info():
    with open("./tests/data/F_lvr_land_B.csv", "r") as f:
        raw = f.read()

    results = parse_deals_info(raw)
    assert type(results) == tuple
    assert len(results) == 2

    deals, deals_need_checked = results[0], results[1]

    assert len(deals) == len(EXPECTED_DEALS)
    assert len(deals_need_checked) == len(EXPECTED_NEED_CHECKED_DEALS)
    assert deals == EXPECTED_DEALS
    assert deals_need_checked == EXPECTED_NEED_CHECKED_DEALS


def test_parse_incorrect_deals_info():
    # case: have deals need check
    resutls = parse_incorrect_deals_info(EXPECTED_NEED_CHECKED_DEALS)
    assert resutls == EXPECTED_NEED_CHECKED_DEALS_PARSED

    # case: no deals need check
    resutls = parse_incorrect_deals_info([])
    assert resutls == None
