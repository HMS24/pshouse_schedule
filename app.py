import time
import logging
from datetime import datetime, timedelta

from pshouse_schedule import scheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from pshouse_schedule.jobs import (
    SCHEDULED_JOBS,
    JOBS,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)10.19s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("debug.log"), logging.StreamHandler()],
)


def event_job_executed_handler(event):
    if event.job_id in (SCHEDULED_JOBS[0]["id"], JOBS[1]["id"]):
        scheduler.add_job(**JOBS[0])


def event_job_error_handler(event):
    if event.job_id == JOBS[0]["id"]:
        if isinstance(event.exception, Exception):
            scheduler.add_job(
                **JOBS[1],
                next_run_time=datetime.now() + timedelta(hours=1),
            )


def main():
    for job in SCHEDULED_JOBS:
        scheduler.add_job(**job)

    scheduler.add_listener(event_job_executed_handler, EVENT_JOB_EXECUTED)
    scheduler.add_listener(event_job_error_handler, EVENT_JOB_ERROR)

    scheduler.start()

    while True:
        time.sleep(2)


def test():
    from pshouse_schedule.processes import process_crawl_of_deals
    process_crawl_of_deals()


if __name__ == "__main__":
    main()
    # test()
