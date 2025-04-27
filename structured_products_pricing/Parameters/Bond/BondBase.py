from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Union
from structured_products_pricing.Parameters.Bond.CashFlow import CashFlow


class BondBase(ABC):
    """
    Abstract base class for bonds.
    Defines the common structure for all types of bonds, including basic attributes
    and required methods for cashflow generation.

    Parameters:
        notional (float): Principal amount of the bond.
        issue_date (str or datetime): Bond issuance date.
        maturity_date (str or datetime): Bond maturity date.
    """

    def __init__(self, notional: float, issue_date: Union[str, datetime], maturity_date: Union[str, datetime]):
        self.product = "Bond"
        self.notional = notional
        self.issue_date = datetime.fromisoformat(issue_date) if isinstance(issue_date, str) else issue_date
        self.maturity_date = datetime.fromisoformat(maturity_date) if isinstance(maturity_date, str) else maturity_date

    @abstractmethod
    def get_cashflows(self) -> List[CashFlow]:
        pass

    def maturity(self):
        cfs = self.get_cashflows()
        return cfs[-1].date if cfs else None
