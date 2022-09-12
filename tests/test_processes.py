import json
import shutil
from datetime import datetime
from unittest import mock

from tests.mock import (
    MockConfig,

    MOCK_RESOURCES_FOLDER,
    MOCK_CHECK_FOLDER,
    EXPECTED_NEED_CHECKED_DEALS_PARSED,

    mock_fetch_deals,
    mock_parse_deals_info,
    mock_parse_incorrect_deals_info,
)
from pshouse_schedule.processes import crawl_deals


@mock.patch("pshouse_schedule.processes.RESOURCES_FOLDER", MOCK_RESOURCES_FOLDER)
@mock.patch("pshouse_schedule.processes.CHECK_FOLDER", MOCK_CHECK_FOLDER)
@mock.patch("pshouse_schedule.processes.config", MockConfig)
@mock.patch("pshouse_schedule.storage.config", MockConfig)
@mock.patch("pshouse_schedule.processes.fetch_deals", mock_fetch_deals)
@mock.patch("pshouse_schedule.processes.parse_deals_info", mock_parse_deals_info)
@mock.patch("pshouse_schedule.processes.parse_incorrect_deals_info", mock_parse_incorrect_deals_info)
@mock.patch("pshouse_schedule.processes.load_into_database")
@mock.patch("pshouse_schedule.processes.generate_saved_filename", return_value="20220901_F_lvr_land_B.csv")
def test_crawl_deals(
        load_into_database_mocker,
        generate_saved_filename_mocker,
):
    # case: success
    _set_up()

    crawl_deals()

    today = datetime.now().strftime("%Y%m%d")
    target_filename = MOCK_RESOURCES_FOLDER.joinpath(
        MockConfig.STORAGE_BUCKET_NAME,
        "20220901_F_lvr_land_B.csv",
    )
    assert target_filename.exists()

    with open(target_filename, "r", encoding="utf-8-sig") as f:
        saved_data = f.read()
    assert saved_data == mock_fetch_deals()

    check_filename = MOCK_RESOURCES_FOLDER.joinpath(
        "check",
        "20220901_F_lvr_land_B.json",
    )
    assert check_filename.exists()

    with open(check_filename, "r", encoding="utf-8-sig") as f:
        saved_data = json.loads(f.read())
    assert saved_data == EXPECTED_NEED_CHECKED_DEALS_PARSED

    _tear_down()


def _set_up():
    try:
        shutil.rmtree(MOCK_RESOURCES_FOLDER)
    except FileNotFoundError:
        pass

    MOCK_RESOURCES_FOLDER.mkdir(parents=True, exist_ok=True)
    MOCK_CHECK_FOLDER.mkdir(parents=True, exist_ok=True)


def _tear_down():
    shutil.rmtree(MOCK_RESOURCES_FOLDER)
