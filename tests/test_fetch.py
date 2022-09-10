from unittest import mock

from pshouse_schedule.fetch import fetch_deals
from tests.mock import mock_request_deals, mock_request_deals_failed


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
        assert len(results) == 648
        assert "檔案不存在" in results
