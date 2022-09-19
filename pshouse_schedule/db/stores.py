from sqlalchemy.sql import text

from pshouse_schedule.db.models import Deal as DealModel


class Deal:

    def __init__(self, session):
        self._session = session

    def bulk_insert(self, rows):
        with self._session() as session:
            session.bulk_insert_mappings(DealModel, rows)
            session.commit()

    def last(self):
        with self._session() as session:
            projections = (DealModel.id, DealModel.created_at)

            return session.query(*projections).order_by(DealModel.id.desc()).first()

    def truncate(self):
        with self._session() as session:
            session.execute(f"truncate {DealModel.__tablename__};")
            session.commit()


class DealStatistics:

    def __init__(self, session):
        self._session = session

    def insert_or_update(self):
        with self._session() as session:
            with open("pshouse_schedule/db/sql/insert_or_update_deal_statistics.sql", "r") as f:
                statement = text(f.read())

                session.execute(statement)
                session.commit()
