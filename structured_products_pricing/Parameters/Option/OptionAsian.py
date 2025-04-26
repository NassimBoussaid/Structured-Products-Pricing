from structured_products_pricing.Parameters.Option.OptionBase import OptionBase
from datetime import datetime
import numpy as np

class OptionAsian(OptionBase):
    """
    Class to handle Asian option parameters, extending from OptionBase.
    """
    def __init__(self, option_type: str, strike: float, maturity_date: datetime, asianing_frequency: str):
        """
        Initializes an Asian option.

        Parameters:
        - option_type: str. "call" or "put".
        - strike: float. Strike price of the option.
        - maturity_date: datetime. The maturity date of the option.
        - asianing_frequency: str. Frequency of the averaging.
        """
        super().__init__(option_type, strike, maturity_date)
        self.option_name: str = "Asian"
        self.asianing_frequency = asianing_frequency

    def payoff(self, und_price: np.array) -> np.array:
        """
        Computes the payoff of the Asian option at a given underlying price path.

        Parameters:
        - und_price: np.array. Array of underlying prices along each path.

        Returns:
        - np.array. Payoff values.
        """
        return np.maximum(0, (np.mean(und_price, axis=1) - self.strike) * (1 if self.is_call() else -1))