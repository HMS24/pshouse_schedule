import time
import logging

from apscheduler.schedulers.background import BackgroundScheduler
from presale.process import process_actual_price_registration

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)10.19s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("debug.log"), logging.StreamHandler()],
)


def main():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        id="crawl_presale_actual_price_registration",
        func=process_actual_price_registration,
        trigger="cron",
        year="*",
        month="*",
        day="1, 11, 21",
        hour="10",
        minute="0",
    )
    scheduler.start()

    # This is here to simulate application activity (which keeps the main thread alive).
    while True:
        time.sleep(2)


if __name__ == "__main__":
    main()
