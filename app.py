import time
import logging
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_EXECUTED
from pshouse_schedule.jobs import (
    JOBS,
    CHECK_JOBS,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)10.19s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("debug.log"), logging.StreamHandler()],
)

scheduler = BackgroundScheduler()


def event_job_executed_handler(event):
    if event.job_id == JOBS[0]["id"]:
        scheduler.add_job(**CHECK_JOBS[0], next_run_time=datetime.now())


def main():
    for job in JOBS:
        scheduler.add_job(**job)

    scheduler.add_listener(event_job_executed_handler, EVENT_JOB_EXECUTED)
    scheduler.start()

    while True:
        time.sleep(2)


def test():
    from pshouse_schedule.processes import process_crawl_of_deals
    process_crawl_of_deals()


if __name__ == "__main__":
    main()
    # test()
