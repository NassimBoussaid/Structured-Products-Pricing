from structured_products_pricing.Parameters.Pricer.PricerBase import PricerBase
from structured_products_pricing.Parameters.Bond.BondBase import BondBase
from structured_products_pricing.Parameters.Market import Market
from structured_products_pricing.Utils.Calendar import Calendar
import math
import datetime as datetime


class RatePricerManager:
    """
    Rate Pricer Manager class.
    Handles pricing and accrued interest calculation for fixed or floating rate products
    using simple discounting based on a constant interest rate.

    Parameters:
        MarketObject (Market): Market environment containing the interest rate.
        BondObject (BondBase): FixedRateBond, FloatingRateBond, or similar rate product.
        pricing_date (datetime): Date at which pricing is performed.

    Methods:
        accrued_interest() -> float:
            Estimates accrued interest from the last coupon date to the pricing date.
        compute_price(clean: bool = False) -> float:
            Computes the discounted price (dirty or clean) of the bond.
    """

    def __init__(self, MarketObject: Market, BondObject: BondBase, pricing_date: datetime):
        self.Market = MarketObject
        self.Product = BondObject
        self.pricing_date = pricing_date

    def accrued_interest(self) -> float:

        past = [d for d in self.Product.calendar.observation_dates if d <= self.pricing_date]
        if not past:
            return 0.0

        last_coupon = max(past)
        accrual = self.Product.calendar.year_fraction(last_coupon, self.pricing_date, self.Product.day_count)

        if hasattr(self.Product, 'coupon_rate'):  # Fixed Rate Bond
            rate = self.Product.coupon_rate
        elif hasattr(self.Product, 'index_curve'):  # Floating Rate Bond
            t = self.Product.calendar.year_fraction(self.Product.issue_date, last_coupon, 'act/365.25')
            rate = self.Product.index_curve.get_yield(t) + self.Product.spread
        else:
            rate = 0.0

        return self.Product.notional * rate * accrual

    def compute_price(self, clean: bool = False) -> float:
        calendar = Calendar(start_date=self.Product.issue_date, end_date=self.Product.maturity_date)
        dirty = 0.0
        for cf in self.Product.get_cashflows():
            t = calendar.year_fraction(self.pricing_date, cf.date, self.Product.day_count)
            df = math.exp(-self.Market.int_rate * t)
            dirty += cf.amount * df

        if clean and hasattr(self.Product, 'calendar'):
            accrued = self.accrued_interest()
            return dirty - accrued

        return dirty
