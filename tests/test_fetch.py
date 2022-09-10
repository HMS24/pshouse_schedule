import os
from unittest import mock

from pshouse_schedule.fetch import (
    fetch_deals,
    is_resource_updated,
)
from tests.mock import (
    mock_request_deals,
    mock_request_deals_failed,
    mock_request_history_deals_list,
)


def test_fetch_deals():
    # case: success
    with mock.patch("pshouse_schedule.fetch.is_resource_updated", return_value=True), \
            mock.patch("requests.get", mock_request_deals):

        results = fetch_deals()
        assert len(results) == 2846
        assert results[:10] == "\ufeff鄉鎮市區,交易標的"

    # case: failed to fetch
    with mock.patch("pshouse_schedule.fetch.is_resource_updated", return_value=True), \
            mock.patch("requests.get", mock_request_deals_failed):

        results = fetch_deals()
        assert results == None

    # case: failed to fetch - resources havn't been updated
    with mock.patch("pshouse_schedule.fetch.is_resource_updated", return_value=False):

        results = fetch_deals()
        assert results == None


def test_is_resource_updated():
    output_dir = "./tests/data/results"

    # case success
    with mock.patch("requests.get", mock_request_history_deals_list), \
            mock.patch("pshouse_schedule.config.STORAGE_ROOT_DIR", output_dir):

        for file in os.listdir(output_dir):
            os.remove(f"{output_dir}/{file}")

        assert is_resource_updated() == True
