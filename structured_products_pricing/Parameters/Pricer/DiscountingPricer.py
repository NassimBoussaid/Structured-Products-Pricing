from datetime import datetime
from structured_products_pricing.Parameters.Pricer.PricerBase import PricerBase


class DiscountingPricer(PricerBase):
    def __init__(self, pricing_date: datetime, day_count: str = 'act/365.25'):
        super().__init__(pricing_date)
        self.pricer_name = 'DiscountingPricer'
        self.day_count = day_count

    @staticmethod
    def _year_fraction(start: datetime, end: datetime, convention: str) -> float:
        days = (end - start).days
        conv = convention.lower()
        if conv == '30/360':
            d1, d2 = min(start.day, 30), min(end.day, 30)
            return ((end.year - start.year) * 360 + (end.month - start.month) * 30 + (d2 - d1)) / 360
        if conv == 'act/360':
            return days / 360
        return days / 365.25

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

    def price(self, product, market, clean: bool = False) -> float:
        dirty = 0.0
        for cf in product.get_cashflows():
            t = self._year_fraction(self.pricing_date, cf.date, self.day_count)
            df = market.discount_curve.discount_factor(t)
            dirty += cf.amount * df

        if clean and hasattr(product, 'calendar'):
            accrued = self.accrued_interest(product)
            return dirty - accrued

        return dirty
