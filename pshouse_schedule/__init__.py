from apscheduler.schedulers.background import BackgroundScheduler

import pshouse_schedule.config as config
from pshouse_schedule.db.database import Database

db = Database(
    uri=config.SQLALCHEMY_DATABASE_URI,
    engine_options=config.SQLALCHEMY_ENGINE_OPTIONS,
)
scheduler = BackgroundScheduler(
    timezone=config.SCHEDULER_TIMEZONE,
)
