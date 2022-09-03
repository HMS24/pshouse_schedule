import logging

import pshouse_schedule.config as config
from pshouse_schedule.db.database import Database
from pshouse_schedule.db.stores import Deal

logger = logging.getLogger()
db = Database(config.DATABASE_URI)


def load_into_database(rows):
    logger.info("   step: load_into_database")

    deal = Deal(db.session)

    try:
        deal.bulk_insert(rows)
    except Exception as e:
        logger.warning(f"   load error: {repr(e)}")
