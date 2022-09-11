import os
import shutil
from unittest import mock
from pathlib import Path

from pshouse_schedule.fetch import (
    fetch_deals,
    have_resources_been_updated,
)
from tests.mock import (
    mock_request_deals,
    mock_request_deals_failed,
    mock_request_history_deals_list,
)


def test_fetch_deals():
    # case: success
    with mock.patch("pshouse_schedule.fetch.have_resources_been_updated", return_value=True), \
            mock.patch("requests.get", mock_request_deals):

        results = fetch_deals()
        assert len(results) == 1579
        assert results[:10] == "\ufeff鄉鎮市區,交易標的"

    # case: failed to fetch
    with mock.patch("pshouse_schedule.fetch.have_resources_been_updated", return_value=True), \
            mock.patch("requests.get", mock_request_deals_failed):

        results = fetch_deals()
        assert results == None

    # case: failed to fetch - resources havn't been updated
    with mock.patch("pshouse_schedule.fetch.have_resources_been_updated", return_value=False):
        results = fetch_deals()
        assert results == None


def test_have_resources_been_updated():
    output_dir = "./tests/data/results"
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # case: empty results, True
    with mock.patch("requests.get", mock_request_history_deals_list), \
            mock.patch("pshouse_schedule.config.STORAGE_ROOT_DIR", output_dir):

        _remove_files_from_dir(output_dir)
        assert have_resources_been_updated() == True

    # case: have been updated, True
    with mock.patch("requests.get", mock_request_history_deals_list), \
            mock.patch("pshouse_schedule.config.STORAGE_ROOT_DIR", output_dir):

        _remove_files_from_dir(output_dir)
        _add_file_to_dir(output_dir, "20220721_F_lvr_land_B.csv")
        _add_file_to_dir(output_dir, "20220801_F_lvr_land_B.csv")
        _add_file_to_dir(output_dir, "20220811_F_lvr_land_B.csv")
        _add_file_to_dir(output_dir, "20220821_F_lvr_land_B.csv")

        assert have_resources_been_updated() == True

        _remove_files_from_dir(output_dir)

    # case: havn't been updated, False
    with mock.patch("requests.get", mock_request_history_deals_list), \
            mock.patch("pshouse_schedule.config.STORAGE_ROOT_DIR", output_dir):

        _remove_files_from_dir(output_dir)
        _add_file_to_dir(output_dir, "20220821_F_lvr_land_B.csv")
        _add_file_to_dir(output_dir, "20220901_F_lvr_land_B.csv")

        assert have_resources_been_updated() == False

        _remove_files_from_dir(output_dir)

    shutil.rmtree(output_dir)


def _remove_files_from_dir(dir_path):
    for filename in os.listdir(dir_path):
        os.remove(f"{dir_path}/{filename}")


def _add_file_to_dir(dir_path, filename):
    open(f"{dir_path}/{filename}", "w").close()
