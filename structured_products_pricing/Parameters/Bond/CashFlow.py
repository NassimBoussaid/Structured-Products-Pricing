from dataclasses import dataclass
from datetime import datetime

@dataclass
class CashFlow:
    """
    CashFlow dataclass.
    Represents a single cashflow occurring at a specific date, with an associated amount.

    Attributes:
        date (datetime): The date on which the cashflow occurs.
        amount (float): The monetary value of the cashflow.
    """
    date: datetime
    amount: float