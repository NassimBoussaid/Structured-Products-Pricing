# products/rate/FloatingRateBond.py
from datetime import datetime
from typing import Union, List
from structured_products_pricing.Products.Bond.BondBase import BondBase
from structured_products_pricing.Products.Bond.CashFlow import CashFlow
from structured_products_pricing.Utils.Calendar import Calendar


class FloatingRateBond(BondBase):
    """
    Obligation à taux variable (Floating Rate Bond).

    :param notional: montant nominal
    :param issue_date: date d'émission
    :param maturity_date: date d'échéance
    :param index_curve: objet RateCurve ou RateFlat pour calculer les taux d'intérêt futurs
    :param spread: marge additive au-dessus de l'index
    :param frequency: fréquence des coupons ('annual', 'semiannual', etc.)
    :param day_count: convention de day count pour accrual ('30/360', 'act/360', 'act/365.25')
    :param calendar_region: région pour le calendrier de trading
    :param business_day_convention: convention de jour ouvré
    :param end_of_month: utiliser dropdown EOM
    """

    def __init__(
            self,
            notional: float,
            issue_date: Union[str, datetime],
            maturity_date: Union[str, datetime],
            index_curve,
            spread: float = 0.0,
            frequency: str = 'yearly',
            day_count: str = 'act/365.25'
    ):
        super().__init__(notional=notional, issue_date=issue_date, maturity_date=maturity_date)
        self.index_curve = index_curve
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
