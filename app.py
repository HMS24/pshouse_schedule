import time
import logging

from apscheduler.events import (
    EVENT_JOB_EXECUTED,
    EVENT_JOB_ERROR,
)

from pshouse_schedule import scheduler
from pshouse_schedule.jobs import SCHEDULED_JOBS
from pshouse_schedule.jobs import (
    event_job_error_handler,
    event_job_executed_handler,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)10.19s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("debug.log"), logging.StreamHandler()],
)


def main():
    for job in SCHEDULED_JOBS.values():
        scheduler.add_job(**job)

    scheduler.add_listener(event_job_executed_handler, EVENT_JOB_EXECUTED)
    scheduler.add_listener(event_job_error_handler, EVENT_JOB_ERROR)

    scheduler.start()

    while True:
        time.sleep(3600)


if __name__ == "__main__":
    main()
