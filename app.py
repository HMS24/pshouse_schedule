import time
import logging

from apscheduler.schedulers.background import BackgroundScheduler
from pshouse_schedule.jobs import JOBS

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)10.19s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("debug.log"), logging.StreamHandler()],
)


def main():
    scheduler = BackgroundScheduler()

    for job in JOBS:
        scheduler.add_job(**job)
    scheduler.start()

    while True:
        time.sleep(2)


def test():
    from pshouse_schedule.processes import process_crawl_of_deals
    process_crawl_of_deals()


if __name__ == "__main__":
    # main()
    test()
