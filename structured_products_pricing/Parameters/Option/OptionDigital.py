from structured_products_pricing.Parameters.Option.OptionBase import OptionBase
from datetime import datetime
import numpy as np

class OptionDigital(OptionBase):
    """
    Class to handle Digital option parameters, extending from OptionBase.
    """
    def __init__(self, option_type: str, strike: float, maturity_date: datetime):
        """
        Initializes a Digital option.

        Parameters:
        - option_type: str. "call" or "put".
        - strike: float. Strike price of the option.
        - maturity_date: datetime. The maturity date of the option.
        """
        super().__init__(option_type, strike, maturity_date)
        self.option_name: str = "Digital"

    def payoff(self, und_price: np.array) -> np.array:
        """
        Computes the payoff of the Digital option at a given underlying price.

        Parameters:
        - und_price: np.array. Array of underlying prices at maturity.

        Returns:
        - np.array. Payoff values.
        """
        return np.where(und_price > self.strike, 1, 0)