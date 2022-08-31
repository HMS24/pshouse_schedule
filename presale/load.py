import logging

from presale.db.database import Database
from presale.db.stores import NewTaipeiCityRepository
from presale.db.services import NewTaipeiCityService

logger = logging.getLogger()
db = Database("mysql+pymysql://root:password@localhost:3306/pshouse")


def load_into_database(rows):
    logger.info("   step: load_into_database")

    service = NewTaipeiCityService(
        session_factory=db.session,
        repository_cls=NewTaipeiCityRepository,
    )

    try:
        service.create_pre_sale_house_transactions(rows)
    except Exception as e:
        logger.warning(f"   load error: {repr(e)}")
