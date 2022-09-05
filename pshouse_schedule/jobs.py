from pshouse_schedule.processes import (
    process_crawl_of_deals,
    process_crawl_of_deals_check,
)

SCHEDULED_JOBS = [
    {
        "id": "crawl_deals_schedule",
        "func": process_crawl_of_deals,
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
        "func": process_crawl_of_deals_check,
    },
    {
        "id": "crawl_deals_once",
        "func": process_crawl_of_deals,
    },
]
