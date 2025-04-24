from datetime import datetime

from structured_products_pricing.Parameters.Pricer.DiscountingPricer import DiscountingPricer
from structured_products_pricing.Utils.Calendar import Calendar


class RatePricer(DiscountingPricer):
    """
        Pricer par actualisation pour tous les produits de taux.
        Hérite de DiscountingPricer pour récupérer :
          - self.pricing_date
          - self.day_count
        """

    def __init__(self, pricing_date: datetime, day_count: str = 'act/365.25'):
        super().__init__(pricing_date, day_count)

    def accrued_interest(self, product) -> float:
        """
        Estime les intérêts courus pour Fixed ou Floating Rate Bond.
        Nécessite que le produit ait :
         - product.calendar
         - product.day_count
         - coupon_rate ou index_curve + spread
        """
        past = [d for d in product.calendar.observation_dates if d <= self.pricing_date]
        if not past:
            return 0.0

        last_coupon = max(past)
        accrual = product.calendar.year_fraction(last_coupon, self.pricing_date, product.day_count)

        if hasattr(product, 'coupon_rate'):  # Fixed Rate Bond
            rate = product.coupon_rate
        elif hasattr(product, 'index_curve'):  # Floating Rate Bond
            t = product.calendar.year_fraction(product.issue_date, last_coupon, 'act/365.25')
            rate = product.index_curve.get_yield(t) + product.spread
        else:
            rate = 0.0

        return product.notional * rate * accrual

    def compute_price(self, product, market, clean: bool = False) -> float:
        calendar = Calendar(start_date=product.issue_date, end_date=product.maturity_date)
        dirty = 0.0
        for cf in product.get_cashflows():
            t = calendar.year_fraction(self.pricing_date, cf.date, self.day_count)
            df = market.discount_curve.discount_factor(t)
            dirty += cf.amount * df

        if clean and hasattr(product, 'calendar'):
            accrued = self.accrued_interest(product)
            return dirty - accrued

        return dirty
