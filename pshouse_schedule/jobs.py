from datetime import datetime, timedelta

from pshouse_schedule import scheduler
from pshouse_schedule.processes import (
    crawl_deals,
    check_deals_crawled,
)
from pshouse_schedule.exceptions import NotUpdatedException

CRAWL_DEALS_SCHEDULE = "crawl_deals_schedule"
CHECK_AFTER_DEALS_CRAWLED = "check_after_deals_crawled"
CRAWL_DEALS_ONCE = "crawl_deals_once"

SCHEDULED_JOBS = {
    CRAWL_DEALS_SCHEDULE: {
        "id": CRAWL_DEALS_SCHEDULE,
        "func": crawl_deals,
        "trigger": "cron",
        "year": "*",
        "month": "*",
        "day": "1, 11, 21",
        "hour": "10",
        "minute": "0",
    }
}

JOBS = {
    CHECK_AFTER_DEALS_CRAWLED: {
        "id": CHECK_AFTER_DEALS_CRAWLED,
        "func": check_deals_crawled
    },
    CRAWL_DEALS_ONCE: {
        "id": CRAWL_DEALS_ONCE,
        "func": crawl_deals,
    }
}


def event_job_executed_handler(event):
    if event.job_id in (CRAWL_DEALS_SCHEDULE, CRAWL_DEALS_ONCE):
        scheduler.add_job(**JOBS[CHECK_AFTER_DEALS_CRAWLED])


def event_job_error_handler(event):
    if event.job_id == CHECK_AFTER_DEALS_CRAWLED:
        if isinstance(event.exception, NotUpdatedException):
            scheduler.add_job(
                **JOBS[CRAWL_DEALS_ONCE],
                next_run_time=datetime.now() + timedelta(hours=1),
            )
