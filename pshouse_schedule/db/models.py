import sqlalchemy as sa

from pshouse_schedule.db.database import Base


class Deal(Base):

    __tablename__ = "deals"

    # BigInteger type can't autoincrement for sqlite, due to cpu or memory 的開銷太大
    id = sa.Column(
        sa.BigInteger().with_variant(sa.Integer, "sqlite"),
        primary_key=True,
    )

    # 縣市、地區、交易標的、位置、交易日期
    city = sa.Column(sa.String(3), nullable=False, index=True)
    district = sa.Column(sa.String(8), nullable=False, index=True)
    object_of_transaction = sa.Column(sa.String(16), nullable=False)
    location = sa.Column(sa.String(128), nullable=False)
    transaction_date = sa.Column(sa.DATE, nullable=False, index=True)

    # 樓層、總樓層、主要用途、建物狀態
    level = sa.Column(sa.String(8), nullable=False)
    total_floor_numbers = sa.Column(sa.String(2), nullable=False)
    main_use = sa.Column(sa.String(16), nullable=False)
    building_state = sa.Column(sa.String(16), nullable=False)

    # 土地面積、建物面積、車位面積  (平方公尺)
    land_total_area = sa.Column(sa.Float, nullable=False)
    building_total_area = sa.Column(sa.Float, nullable=False)
    parking_sapce_total_area = sa.Column(sa.Float, nullable=False)

    # 房間數、客餐廳、衛浴
    room = sa.Column(sa.String(1), nullable=False)
    restaurant_and_living_room = sa.Column(sa.String(1), nullable=False)
    bathroom = sa.Column(sa.String(1), nullable=False)

    # 備註、預售案名、預售棟名
    note = sa.Column(sa.String(128), nullable=False)
    build_name = sa.Column(sa.String(32), nullable=False, index=True)
    buildings = sa.Column(sa.String(32), nullable=False)

    # 總價、單價、車位類型、車位價格 (元)
    price = sa.Column(sa.Integer, nullable=False)
    unit_price = sa.Column(sa.Integer, nullable=False)
    parking_sapce_type = sa.Column(sa.String(8), nullable=False)
    parking_sapce_price = sa.Column(sa.Integer, nullable=False)

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


class DealStatistics(Base):

    __tablename__ = "deal_statistics"
    __table_args__ = (
        sa.UniqueConstraint(
            "city",
            "district",
            "year",
            "month",
            "build_name",
            "room",
            name="uc_city_district_year_month_buildname_room",
        ),
    )

    id = sa.Column(
        sa.Integer,
        primary_key=True,
    )
    city = sa.Column(
        sa.String(3),
        nullable=False,
    )
    district = sa.Column(
        sa.String(8),
        nullable=False,
    )
    year = sa.Column(
        sa.String(4),
        nullable=False,
    )
    month = sa.Column(
        sa.String(2),
        nullable=False,
    )
    build_name = sa.Column(
        sa.String(32),
        nullable=False,
    )
    room = sa.Column(
        sa.String(1),
        nullable=False,
    )
    count_num = sa.Column(
        sa.Integer,
        nullable=False,
    )
    avg_total_price = sa.Column(
        sa.Integer,
        nullable=False,
    )
    avg_house_price = sa.Column(
        sa.Integer,
        nullable=False,
    )
    avg_house_unit_price = sa.Column(
        sa.Integer,
        nullable=False,
    )
    created_at = sa.Column(
        sa.DateTime(timezone=True),
        server_default=sa.func.now(),
    )
    updated_at = sa.Column(
        sa.DateTime(timezone=True),
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
    )
