import logging
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger()
Base = declarative_base()


class Database:
    def __init__(self, uri, engine_options):
        self._engine = create_engine(uri, **engine_options)
        self._session_factory = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self._engine,
        )

        if uri.startswith("sqlite"):
            self.create_tables()

    def create_tables(self):
        Base.metadata.create_all(self._engine)

    @contextmanager
    def session(self):
        session = self._session_factory()
        try:
            yield session
        except Exception as e:
            logger.warn(f"EXCEPTION: Session rollback, {repr(e)}"))
            session.rollback()

            raise e
        finally:
            session.close()
