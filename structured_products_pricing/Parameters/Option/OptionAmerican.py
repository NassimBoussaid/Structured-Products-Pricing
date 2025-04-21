import numpy as np
from datetime import datetime
from structured_products_pricing.Parameters.Option.OptionBase import OptionBase

class OptionAmerican(OptionBase):
    """
    Class to handle American option parameters.
    """
    def __init__(self, option_type: str, strike: float, maturity_date: datetime, regression_type: str,
                 regression_degree: int):
        super().__init__(option_type, strike, maturity_date)
        self.option_name: str = "American"
        self.regression_type = regression_type
        self.regression_degree = regression_degree

    def payoff(self, und_price: np.array) -> np.array:
        return np.maximum(0, (und_price - self.strike) * (1 if self.is_call() else -1))