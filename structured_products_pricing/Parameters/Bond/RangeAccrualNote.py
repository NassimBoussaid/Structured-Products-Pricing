from datetime import datetime
from typing import Union, List
from structured_products_pricing.Parameters.Bond.BondBase import BondBase
from structured_products_pricing.Parameters.Bond.CashFlow import CashFlow
from structured_products_pricing.Utils.Calendar import Calendar

class RangeAccrualNote(BondBase):
    """
    Range Accrual Note: note de taux qui verse un coupon proportionnel au ratio de jours
    où le taux indexé reste dans une fourchette [low, high] sur chaque période de coupon.

    :param notional: montant nominal
    :param issue_date: date d'émission
    :param maturity_date: date d'échéance
    :param index_curve: objet avec get_yield(t)
    :param coupon_rate: taux de coupon annuel fixé (appliqué avant ratio)
    :param low: borne basse du range
    :param high: borne haute du range
    :param participation: proportion appliquée au ratio de jours
    :param frequency: fréquence de paiement des coupons
    :param day_count: convention day count pour fraction d'année
    """

    def __init__(
            self,
            notional: float,
            issue_date: Union[str, datetime],
            maturity_date: Union[str, datetime],
            index_curve,
            coupon_rate: float,
            low: float,
            high: float,
            participation: float = 1.0,
            frequency: str = 'annual',
            day_count: str = 'act/365.25'
    ):
        super().__init__(notional)
        self.issue_date = datetime.fromisoformat(issue_date) if isinstance(issue_date, str) else issue_date
        self.maturity_date = datetime.fromisoformat(maturity_date) if isinstance(maturity_date, str) else maturity_date
        self.index_curve = index_curve
        self.coupon_rate = coupon_rate
        self.low = low
        self.high = high
        self.participation = participation
        self.day_count = day_count
        self.calendar = Calendar(
            frequency=frequency,
            start_date=self.issue_date,
            end_date=self.maturity_date,
        )

    def get_cashflows(self) -> List[CashFlow]:
        coupon_dates = [d for d in self.calendar.observation_dates if d > self.issue_date]
        cfs: List[CashFlow] = []
        prev = self.issue_date

        for coupon_date in coupon_dates:
            days = [d for d in self.calendar.all_dates if prev < d <= coupon_date]
            in_range_days = 0
            for d in days:
                t = (d - self.issue_date).days / 365.25
                rate = self.index_curve.get_yield(t)
                if self.low <= rate <= self.high:
                    in_range_days += 1
            ratio = in_range_days / len(days) if days else 0.0
            accrual = self.calendar.year_fraction(prev, coupon_date, self.day_count)
            base_coupon = self.notional * self.coupon_rate * accrual
            amount = base_coupon * ratio * self.participation
            cfs.append(CashFlow(date=coupon_date, amount=amount))
            prev = coupon_date

        # remboursement du nominal sur le dernier coupon
        if cfs:
            cfs[-1].amount += self.notional
        return cfs
