from datetime import datetime
from typing import Union, List
from .BondBase import BondBase
from .CashFlow import CashFlow


class ZeroCouponBond(BondBase):
    def __init__(self, notional: float, maturity_date: Union[str, datetime]):
        super().__init__(notional=notional)
        self.maturity_date = datetime.fromisoformat(maturity_date) if isinstance(maturity_date, str) else maturity_date

    def get_cashflows(self) -> List[CashFlow]:
        return [CashFlow(date=self.maturity_date, amount=self.notional)]
