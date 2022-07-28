from datetime import datetime

from pydantic import BaseModel, validator


class ActualPriceRegistrationInfo(BaseModel):
    district: str = ""
    object_of_transaction: str = ""
    location: str = ""
    transaction_date: datetime = None
    level: str = ""
    total_floor_numbers: str = ""
    main_use: str = ""
    building_state: str = ""
    room: str = ""
    restaurant_and_living_room: str = ""
    bathroom: str = ""
    land_total_area: float = 0.00
    building_total_area: float = 0.00
    parking_sapce_total_area: float = 0.00
    price: int = 0
    unit_price: int = 0
    parking_sapce_type: str = ""
    parking_sapce_price: int = 0
    note: str = ""
    build_name: str = ""
    buildings: str = ""

    @validator("bathroom", "room", "restaurant_and_living_room")
    def validate_room_numbers(cls, val):
        assert int(val) < 10, f"There are too many rooms. {val} rooms?"
        return val
