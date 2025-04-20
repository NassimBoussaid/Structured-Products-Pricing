import numpy as np
from datetime import datetime
from Parameters.Option.OptionBase import OptionBase

class OptionDigital(OptionBase):
    """
    Class to handle Digital option parameters.
    """
    def __init__(self, option_type: str, strike: float, maturity_date: datetime):
        super().__init__(option_type, strike, maturity_date)
        self.option_name: str = "Digital"

    def payoff(self, und_price: np.array) -> np.array:
        return np.where(und_price > self.strike, 1, 0)