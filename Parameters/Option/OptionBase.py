import numpy as np
from datetime import datetime
from abc import ABC, abstractmethod

class OptionBase(ABC):
    """
    Abstract class to handle option parameters.
    """
    def __init__(self, option_type: str, strike: float, maturity_date: datetime):
        self.option_name: str = None
        self.option_type: str = option_type
        self.strike: float = strike
        self.maturity_date: datetime = maturity_date
        self.time_to_maturity: float = None

    def is_call(self) -> bool:
        return self.option_type.lower() == "call"

    def is_put(self) -> bool:
        return self.option_type.lower() == "put"

    @abstractmethod
    def payoff(self, und_price: np.array) -> np.array:
        return max(0, (und_price - self.strike) * (1 if self.is_call() else -1))