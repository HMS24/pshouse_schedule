import time
import logging

from apscheduler.schedulers.background import BackgroundScheduler
from presale.jobs import JOBS

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


if __name__ == "__main__":
    main()
