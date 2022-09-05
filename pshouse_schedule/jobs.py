from pshouse_schedule.processes import (
    crawl_deals,
    check_deals_crawled,
)

SCHEDULED_JOBS = [
    {
        "id": "crawl_deals_schedule",
        "func": crawl_deals,
        "trigger": "cron",
        "year": "*",
        "month": "*",
        "day": "1, 11, 21",
        "hour": "10",
        "minute": "0",
    },
]

JOBS = [
    {
        "id": "check_after_deals_crawled",
        "func": check_deals_crawled,
    },
    {
        "id": "crawl_deals_once",
        "func": crawl_deals,
    },
]
