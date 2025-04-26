from abc import ABC, abstractmethod
from datetime import datetime
import numpy as np

class OptionBase(ABC):
    """
    Abstract base class to handle common option parameters.
    """
    def __init__(self, option_type: str, strike: float, maturity_date: datetime):
        """
        Initializes basic attributes for an option.

        Parameters:
        - option_type: str. "call" or "put".
        - strike: float. Strike price of the option.
        - maturity_date: datetime. Maturity date of the option.
        """
        self.product: str = "Option"
        self.option_name: str = None
        self.option_type: str = option_type
        self.strike: float = strike
        self.maturity_date: datetime = maturity_date
        self.time_to_maturity: float = None

    def is_call(self) -> bool:
        """
        Checks if the option type is "call".

        Returns:
        - bool. True if call option, False otherwise.
        """
        return self.option_type.lower() == "call"

    def is_put(self) -> bool:
        """
        Checks if the option type is "put".

        Returns:
        - bool. True if put option, False otherwise.
        """
        return self.option_type.lower() == "put"

    @abstractmethod
    def payoff(self, und_price: np.array) -> np.array:
        """
        Abstract method to compute the option payoff. Must be implemented by each subclass.

        Parameters:
        - und_price: np.array. Array of underlying prices.

        Returns:
        - np.array. Payoff values.
        """
        return max(0, (und_price - self.strike) * (1 if self.is_call() else -1))