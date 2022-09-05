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
