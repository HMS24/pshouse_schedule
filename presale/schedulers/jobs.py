from presale.crawlers.process import process_actual_price_registration


JOBS = [
    {
        "id": "crawl_actual_price_registration",
        "func": process_actual_price_registration,
        "trigger": "cron",
        "year": "*",
        "month": "*",
        "day": "1, 11, 21",
        "hour": "10",
        "minute": "0",
    },
]
