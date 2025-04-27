from structured_products_pricing.Parameters.Bond.BondBase import BondBase
from structured_products_pricing.Parameters.Bond.CashFlow import CashFlow
from structured_products_pricing.Parameters.Bond.BondFixedRate import FixedRateBond
from structured_products_pricing.Parameters.Bond.BondFloatingRate import FloatingRateBond
from collections import defaultdict
from datetime import datetime
from typing import Union, List

class InterestRateSwap(BondBase):
    """
    Interest Rate Swap (IRS) combinant une patte fixe et une patte flottante.

    La patte fixe est payée (montants négatifs), la patte flottante est reçue (montants positifs).

    :param notional: montant du nominal
    :param issue_date: date d'initiation du swap
    :param maturity_date: date d'échéance du swap
    :param fixed_rate: taux fixe payé périodiquement
    :param index_curve: courbe d'index pour la patte flottante
    :param spread: marge ajoutée au taux index pour la patte flottante
    :param frequency: fréquence des paiements pour les deux pattes
    :param day_count: convention day count pour accrual
    """

    def __init__(
            self,
            notional: float,
            issue_date: Union[str, datetime],
            maturity_date: Union[str, datetime],
            fixed_rate: float,
            spread: float = 0.0,
            frequency: str = 'yearly',
            day_count: str = 'act/365.25'
    ):
        super().__init__(notional=notional, issue_date=issue_date, maturity_date=maturity_date)
        # création des deux legs
        self.fixed_leg = FixedRateBond(
            notional=notional,
            issue_date=issue_date,
            maturity_date=maturity_date,
            coupon_rate=fixed_rate,
            frequency=frequency,
            day_count=day_count
        )
        self.float_leg = FloatingRateBond(
            notional=notional,
            issue_date=issue_date,
            maturity_date=maturity_date,
            spread=spread,
            frequency=frequency,
            day_count=day_count
        )
        self.day_count = day_count

    def get_cashflows(self) -> List[CashFlow]:
        """
        Combine et net des cashflows de la patte flottante (reçue) et de la patte fixe (payée).
        """
        float_cfs = self.float_leg.get_cashflows()
        fixed_cfs = self.fixed_leg.get_cashflows()
        cf_map = defaultdict(float)
        for cf in float_cfs:
            cf_map[cf.date] += cf.amount  # montant positif (on reçoit)
        for cf in fixed_cfs:
            cf_map[cf.date] -= cf.amount  # montant négatif (on paie)
        combined = [CashFlow(date=d, amount=amt) for d, amt in sorted(cf_map.items())]
        return [cf for cf in combined if cf.amount != 0.0]
