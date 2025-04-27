from datetime import datetime
from typing import Union, List
from structured_products_pricing.Parameters.Bond.BondBase import BondBase
from structured_products_pricing.Parameters.Bond.CashFlow import CashFlow
from structured_products_pricing.Utils.Calendar import Calendar


class FixedRateBond(BondBase):
    """
    Fixed Rate Bond class.

    Represents a standard bond paying fixed coupons at regular intervals until maturity.

    Parameters:
        notional (float): Principal amount of the bond.
        issue_date (str or datetime): Bond issuance date.
        maturity_date (str or datetime): Bond maturity date.
        coupon_rate (float): Annual fixed coupon rate (as a decimal, e.g., 0.05 for 5%).
        frequency (str, optional): Coupon payment frequency ('annual', 'semiannual', etc.). Defaults to 'yearly'.
        day_count (str, optional): Day count convention ('30/360', 'act/360', 'act/365.25'). Defaults to 'act/365.25'.

    Attributes:
        coupon_rate (float): Fixed annual coupon rate.
        frequency (str): Frequency of coupon payments.
        day_count (str): Day count convention for interest accrual.
        calendar (Calendar): Calendar managing coupon observation dates.
    """

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
