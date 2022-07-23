import logging

from real_.db.database import Database
from real_.db.repositories import NewTaipeiCityRepository
from real_.db.services import NewTaipeiCityService

logger = logging.getLogger()
db = Database('')
db.create_tables()


def load_into_database(rows):
    logger.info('step: load_into_database')

    service = NewTaipeiCityService(
        session_factory=db.session,
        repository_cls=NewTaipeiCityRepository,
    )

    try:
        service.create_pre_sale_house_transactions(rows)
    except Exception as e:
        logger.warning(f'load error: {repr(e)}')
