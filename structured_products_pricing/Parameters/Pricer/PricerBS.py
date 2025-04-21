from datetime import datetime
from structured_products_pricing.Parameters.Pricer.PricerBase import PricerBase

class PricerBS(PricerBase):
    """
    A class to handle pricer parameters for Monte Carlo.
    """
    def __init__(self, pricing_date: datetime):
        super().__init__(pricing_date)
        self.pricer_name: str = "BS"