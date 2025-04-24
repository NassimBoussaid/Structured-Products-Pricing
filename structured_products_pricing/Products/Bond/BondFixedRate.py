from datetime import datetime
from typing import Union, List
from structured_products_pricing.Products.Bond.BondBase import BondBase
from structured_products_pricing.Products.Bond.CashFlow import CashFlow

from structured_products_pricing.Utils.Calendar import Calendar


class FixedRateBond(BondBase):
    def __init__(
            self,
            notional: float,
            issue_date: Union[str, datetime],
            maturity_date: Union[str, datetime],
            coupon_rate: float,
            frequency: str = 'yearly',
            day_count: str = 'act/365.25'):
        super().__init__(notional=notional, issue_date=issue_date, maturity_date=maturity_date)
        self.coupon_rate = coupon_rate
        self.frequency = frequency
        self.day_count = day_count
        self.calendar = Calendar(
            frequency=frequency,
            start_date=self.issue_date,
            end_date=self.maturity_date,
        )

    def get_cashflows(self) -> List[CashFlow]:
        """
        Génère les cashflows coupons et ajoute le remboursement du nominal final.
        La fraction d'année est calculée via `Calendar.year_fraction`.
        """
        dates = [d for d in self.calendar.observation_dates if d > self.issue_date]
        cfs: List[CashFlow] = []
        prev = self.issue_date

        for dt in dates:
            accrual = self.calendar.year_fraction(start=prev, end=dt, convention=self.day_count)
            amount = self.notional * self.coupon_rate * accrual
            cfs.append(CashFlow(date=dt, amount=amount))
            prev = dt
        # Nominal on last date
        if cfs:
            cfs[-1].amount += self.notional
        return cfs
