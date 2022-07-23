from real_.db.models import NewTaipeiCityModel


class NewTaipeiCityRepository:

    def __init__(self, session):
        self._session = session

    def bulk_insert(self, rows):
        self._session.bulk_insert_mappings(NewTaipeiCityModel, rows)
