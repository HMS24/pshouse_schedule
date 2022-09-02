import sqlalchemy as sa

from pshouse_schedule.db.database import Base


class Deal(Base):

    __tablename__ = "deals"

    id = sa.Column(sa.BigInteger, primary_key=True)

    # info
    city = sa.Column(sa.String(3), nullable=False, default="新北市", index=True)
    district = sa.Column(sa.String(8), nullable=False, index=True)
    object_of_transaction = sa.Column(sa.String(16), nullable=False)
    location = sa.Column(sa.String(128), nullable=False)
    transaction_date = sa.Column(sa.DATE, nullable=False, index=True)
    level = sa.Column(sa.String(8), nullable=False)
    total_floor_numbers = sa.Column(sa.String(2), nullable=False)
    building_state = sa.Column(sa.String(16), nullable=False)
    main_use = sa.Column(sa.String(16), nullable=False)

    # area, room and buildings name
    land_total_area = sa.Column(sa.Float, nullable=False)
    building_total_area = sa.Column(sa.Float, nullable=False)
    room = sa.Column(sa.String(1), nullable=False)
    restaurant_and_living_room = sa.Column(sa.String(1), nullable=False)
    bathroom = sa.Column(sa.String(1), nullable=False)
    build_name = sa.Column(sa.String(32), nullable=False, index=True)
    buildings = sa.Column(sa.String(32), nullable=False)

    # car
    parking_sapce_type = sa.Column(sa.String(8), nullable=False)
    parking_sapce_total_area = sa.Column(sa.Float, nullable=False)
    parking_sapce_price = sa.Column(sa.Integer, nullable=False)

    # price
    price = sa.Column(sa.Integer, nullable=False)
    unit_price = sa.Column(sa.Integer, nullable=False)

    note = sa.Column(sa.String(128), nullable=False)

    created_at = sa.Column(sa.DateTime(timezone=True),
                           server_default=sa.func.now())
    updated_at = sa.Column(sa.DateTime(timezone=True),
                           server_default=sa.func.now(), onupdate=sa.func.now())

    def __repr__(self):
        return f"""<DealModel(
            {self.id},
            {self.transaction_date},
            {self.build_name},
            {self.buildings}
        )>"""
