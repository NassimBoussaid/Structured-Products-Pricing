from datetime import datetime
from typing import Union, List
from structured_products_pricing.Parameters.Bond.BondBase import BondBase
from structured_products_pricing.Parameters.Bond.CashFlow import CashFlow

class ZeroCouponBond(BondBase):
    def __init__(self, notional: float, issue_date: Union[str, datetime], maturity_date: Union[str, datetime]):
        super().__init__(notional=notional, issue_date=issue_date, maturity_date=maturity_date)
        self.day_count: str = 'act/365.25'

    def get_cashflows(self) -> List[CashFlow]:
        return [CashFlow(date=self.maturity_date, amount=self.notional)]