from datetime import datetime

class Maturity:
    def __init__(self, value_date: datetime, maturity_date: datetime, convention_date: str):
        self.value_date = value_date
        self.maturity_date = maturity_date
        self.convention_date = convention_date
        self.time_to_maturity = None

    def calculate_time_to_maturity(self):
        pass
