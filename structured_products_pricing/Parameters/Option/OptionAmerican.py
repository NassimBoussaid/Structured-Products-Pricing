from structured_products_pricing.Parameters.Option.OptionBase import OptionBase
from datetime import datetime
import numpy as np

class OptionAmerican(OptionBase):
    """
    Class to handle American option parameters, extending from OptionBase.
    """
    def __init__(self, option_type: str, strike: float, maturity_date: datetime, regression_type: str,
                 regression_degree: int):
        """
        Initializes an American option.

        Parameters:
        - option_type: str. "call" or "put".
        - strike: float. Strike price of the option.
        - maturity_date: datetime. The maturity date of the option.
        - regression_type: str. Type of basis functions for regression.
        - regression_degree: int. Degree of the basis functions for regression.
        """
        super().__init__(option_type, strike, maturity_date)
        self.option_name: str = "American"
        self.regression_type = regression_type
        self.regression_degree = regression_degree

    def payoff(self, und_price: np.array) -> np.array:
        """
        Computes the payoff of the American option at a given underlying price.

        Parameters:
        - und_price: np.array. Array of underlying prices at exercise.

        Returns:
        - np.array. Payoff values.
        """
        return np.maximum(0, (und_price - self.strike) * (1 if self.is_call() else -1))