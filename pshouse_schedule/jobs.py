from pshouse_schedule.processes import (
    process_crawl_of_deals,
    process_crawl_of_deals_check,
)

JOBS = [
    {
        "id": "crawl_deals",
        "func": process_crawl_of_deals,
        "trigger": "cron",
        "year": "*",
        "month": "*",
        "day": "1, 11, 21",
        "hour": "10",
        "minute": "0",
    },
]

CHECK_JOBS = [
    {
        "id": "crawl_deals_check",
        "func": process_crawl_of_deals_check,
    },
]
