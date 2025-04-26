from structured_products_pricing.Parameters.Pricer.PricerBase import PricerBase
from datetime import datetime

class PricerBS(PricerBase):
    """
    Class to handle pricer parameters for Black-Scholes pricing, extending from PricerBase.
    """
    def __init__(self, pricing_date: datetime):
        """
        Initializes a Black-Scholes pricer.

        Parameters:
        - pricing_date: datetime. The date at which pricing is performed.
        """
        super().__init__(pricing_date)
        self.pricer_name: str = "BS"