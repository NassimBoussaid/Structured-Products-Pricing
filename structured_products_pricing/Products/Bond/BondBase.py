from abc import ABC, abstractmethod
from typing import List
from structured_products_pricing.Products.Bond.CashFlow import CashFlow


class BondBase(ABC):
    def __init__(self, notional: float):
        self.notional = notional

    @abstractmethod
    def get_cashflows(self) -> List[CashFlow]:
        pass

    def maturity(self):
        cfs = self.get_cashflows()
        return cfs[-1].date if cfs else None
