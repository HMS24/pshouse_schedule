from pshouse_schedule.processes import process_crawl_of_deals


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
