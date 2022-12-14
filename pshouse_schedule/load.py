import logging

from pshouse_schedule import db
from pshouse_schedule.db.stores import Deal

logger = logging.getLogger()


def load_into_database(rows):
    logger.info("PROCESS: crawl_deals, STEP: load_into_database")

    deal = Deal(db.session)

    try:
        deal.bulk_insert(rows)
    except Exception as e:
        logger.warning(
            f"PROCESS: crawl_deals, STEP: load_into_database, EXCEPTION: load error, {repr(e)}")
