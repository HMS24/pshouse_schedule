import logging
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    sessionmaker,
    scoped_session,
)

logger = logging.getLogger()
Base = declarative_base()


class Database:
    def __init__(self, uri):
        self._engine = create_engine(uri, echo=True)
        self._session_factory = scoped_session(
            sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
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
            logger.warn(f"Session rollback: {repr(e)}")
            session.rollback()
        finally:
            session.close()
