from real_.db.schemas import NewTaipeiCitySchema


class NewTaipeiCityModel(NewTaipeiCitySchema):

    __tablename__ = 'new_taipei_city'

    def __repr__(self):
        return f"""<NewTaipeiCityModel(
            {self.id},
            {self.transaction_date},
            {self.build_name},
            {self.buildings}
        )>"""
