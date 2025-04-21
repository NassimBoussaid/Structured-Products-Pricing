import numpy as np
from datetime import datetime
from structured_products_pricing.Parameters.Option.OptionBase import OptionBase

class OptionAsian(OptionBase):
    """
    Class to handle Asian option parameters.
    """
    def __init__(self, option_type: str, strike: float, maturity_date: datetime, asianing_frequency: str):
        super().__init__(option_type, strike, maturity_date)
        self.option_name: str = "Asian"
        self.asianing_frequency = asianing_frequency

    def payoff(self, und_price: np.array) -> np.array:
        return np.maximum(0, (np.mean(und_price, axis=1) - self.strike) * (1 if self.is_call() else -1))