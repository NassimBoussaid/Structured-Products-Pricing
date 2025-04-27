from datetime import datetime
from typing import Union, List
from structured_products_pricing.Parameters.Bond.BondBase import BondBase
from structured_products_pricing.Parameters.Bond.CashFlow import CashFlow
from structured_products_pricing.Rate.RateCurve import RateCurve
from structured_products_pricing.Utils.Calendar import Calendar


class FloatingRateBond(BondBase):
    """
    Floating Rate Bond class.

    Represents a bond whose coupon payments are linked to a floating interest rate index plus a fixed spread.

    Parameters:
        notional (float): Bond principal amount.
        issue_date (str or datetime): Bond issuance date.
        maturity_date (str or datetime): Bond maturity date.
        spread (float, optional): Fixed spread added to the index rate. Defaults to 0.0.
        frequency (str, optional): Coupon payment frequency ('annual', 'semiannual', etc.). Defaults to 'yearly'.
        day_count (str, optional): Day count convention ('30/360', 'act/360', 'act/365.25'). Defaults to 'act/365.25'.

    Attributes:
        index_curve (RateCurve): Curve used to determine the floating rate at each payment date.
        calendar (Calendar): Calendar managing observation dates and business day adjustments.

    Methods:
        get_cashflows() -> List[CashFlow]:
            Generates future cashflows including coupons and principal repayment,
            based on the floating index curve and spread.
    """

    def __init__(
            self,
            notional: float,
            issue_date: Union[str, datetime],
            maturity_date: Union[str, datetime],
            spread: float = 0.0,
            frequency: str = 'yearly',
            day_count: str = 'act/365.25'
    ):
        super().__init__(notional=notional, issue_date=issue_date, maturity_date=maturity_date)
        self.index_curve = RateCurve(0.01, 0.01, 0.01, 1)
        self.index_curve.compute_yield_curve()
        self.spread = spread
        self.day_count = day_count
        self.calendar = Calendar(
            frequency=frequency,
            start_date=self.issue_date,
            end_date=self.maturity_date,
        )

    def get_cashflows(self) -> List[CashFlow]:
        """
        Génère les cashflows de coupons variables et le remboursement final.
        La méthode calcule pour chaque période:
          coupon = notional * (index_rate + spread) * accrual_fraction
        où index_rate est obtenu via index_curve (ici traité en tant que RateFlat ou RateCurve).
        """
        dates = [d for d in self.calendar.observation_dates if d > self.issue_date]
        cfs: List[CashFlow] = []
        prev = self.issue_date

        for dt in dates:
            accrual = self.calendar.year_fraction(prev, dt, self.day_count)

            t = self.calendar.year_fraction(self.issue_date, dt, 'act/365.25')
            idx_rate = self.index_curve.get_yield(t)
            amt = self.notional * (idx_rate + self.spread) * accrual
            cfs.append(CashFlow(date=dt, amount=amt))
            prev = dt

        if cfs:
            cfs[-1].amount += self.notional
        return cfs
