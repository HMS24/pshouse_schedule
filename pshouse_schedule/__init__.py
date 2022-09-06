from apscheduler.schedulers.background import BackgroundScheduler

import pshouse_schedule.config as config
from pshouse_schedule.db.database import Database

db = Database(config.DATABASE_URI)
scheduler = BackgroundScheduler(
    timezone=config.SCHEDULER_TIMEZONE,
)
