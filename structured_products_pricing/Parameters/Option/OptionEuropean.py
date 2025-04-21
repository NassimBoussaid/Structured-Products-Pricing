import numpy as np
from datetime import datetime
from structured_products_pricing.Parameters.Option.OptionBase import OptionBase

class OptionEuropean(OptionBase):
    """
    Class to handle European option parameters.
    """
    def __init__(self, option_type: str, strike: float, maturity_date: datetime):
        super().__init__(option_type, strike, maturity_date)
        self.option_name: str = "European"

    def payoff(self, und_price: np.array) -> np.array:
        return np.maximum(0, (und_price - self.strike) * (1 if self.is_call() else -1))