from structured_products_pricing.Parameters.Pricer.PricerBase import PricerBase
from datetime import datetime

class DiscountingPricer(PricerBase):
    """
    Class to handle simple discounting pricer logic, extending from PricerBase.
    """
    def __init__(self, pricing_date: datetime, day_count: str = "act/365"):
        """
        Initializes a DiscountingPricer.

        Parameters:
        - pricing_date: datetime. The date at which pricing is performed.
        - day_count: str. Day count convention to use for discounting (default: "act/365").
        """
        super().__init__(pricing_date)
        self.pricer_name = 'DiscountingPricer'
        self.day_count = day_count