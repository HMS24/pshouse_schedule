import pshouse_schedule.config as config
from pshouse_schedule.db.database import Database
from apscheduler.schedulers.background import BackgroundScheduler

db = Database(config.DATABASE_URI)
scheduler = BackgroundScheduler()
