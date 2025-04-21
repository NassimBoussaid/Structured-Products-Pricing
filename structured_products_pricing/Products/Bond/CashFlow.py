from dataclasses import dataclass
from datetime import datetime


@dataclass
class CashFlow:
    date: datetime
    amount: float
