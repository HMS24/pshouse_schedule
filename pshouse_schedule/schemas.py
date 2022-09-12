from datetime import datetime

from pydantic import BaseModel, validator


class Deal(BaseModel):

    # 城市、地區、交易標的、位置、交易日期
    city: str = ""
    district: str = ""
    object_of_transaction: str = ""
    location: str = ""
    transaction_date: datetime = None

    # 樓層、總樓層、主要用途、建物狀態
    level: str = ""
    total_floor_numbers: str = ""
    main_use: str = ""
    building_state: str = ""

    # 房間數、客餐廳、衛浴
    room: str = ""
    restaurant_and_living_room: str = ""
    bathroom: str = ""

    # 土地面積、建物面積、車位面積  (平方公尺)
    land_total_area: float = 0.00
    building_total_area: float = 0.00
    parking_sapce_total_area: float = 0.00

    # 總價、單價、車位類型、車位價格 (元)
    price: int = 0
    unit_price: int = 0
    parking_sapce_type: str = ""
    parking_sapce_price: int = 0

    # 備註、預售案名、預售棟名
    note: str = ""
    build_name: str = ""
    buildings: str = ""

    # 房間、客餐廳及衛浴數不會超過 10 間
    @validator("bathroom", "room", "restaurant_and_living_room")
    def validate_room_numbers(cls, val):
        assert int(val) < 10, f"There are too many rooms. {val} rooms?"
        return val
