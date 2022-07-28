from sqlalchemy.sql import func
from sqlalchemy import (
    Column,
    String,
    Float,
    Integer,
    BigInteger,
    DATE,
    DateTime,
)

from presale.db.database import Base


class NewTaipeiCitySchema(Base):

    __abstract__ = True

    id = Column(BigInteger, primary_key=True)

    # info
    district = Column(String(8), nullable=False, index=True)
    object_of_transaction = Column(String(16), nullable=False)
    location = Column(String(128), nullable=False)
    transaction_date = Column(DATE, nullable=False, index=True)
    level = Column(String(8), nullable=False)
    total_floor_numbers = Column(String(2), nullable=False)
    building_state = Column(String(16), nullable=False)
    main_use = Column(String(16), nullable=False)

    # area, room and buildings name
    land_total_area = Column(Float, nullable=False)
    building_total_area = Column(Float, nullable=False)
    room = Column(String(1), nullable=False)
    restaurant_and_living_room = Column(String(1), nullable=False)
    bathroom = Column(String(1), nullable=False)
    build_name = Column(String(32), nullable=False, index=True)
    buildings = Column(String(32), nullable=False)

    # car
    parking_sapce_type = Column(String(8), nullable=False)
    parking_sapce_total_area = Column(Float, nullable=False)
    parking_sapce_price = Column(Integer, nullable=False)

    # price
    price = Column(Integer, nullable=False)
    unit_price = Column(Integer, nullable=False)

    note = Column(String(128), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True),
                        server_default=func.now(), onupdate=func.now())
