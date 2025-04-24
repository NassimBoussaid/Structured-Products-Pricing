from datetime import datetime
from structured_products_pricing.Parameters.Pricer.PricerBase import PricerBase
from structured_products_pricing.Utils.Calendar import Calendar


class DiscountingPricer(PricerBase):
    def __init__(self, pricing_date: datetime, day_count: str = 'act/365.25'):
        super().__init__(pricing_date)
        self.pricer_name = 'DiscountingPricer'
        self.day_count = day_count
