from structured_products_pricing.Parameters.Market import Market
from structured_products_pricing.Parameters.Pricer.PricerBase import PricerBase
from structured_products_pricing.Strategies.StrategyBase import StrategyBase
from datetime import datetime

class StrategyStructuredBase(StrategyBase):
    """
    Base class to define the structure of structured products, extending from StrategyBase.
    """
    def __init__(self, MarketObject: Market, PricerObject: PricerBase, maturity_date: datetime):
        """
        Initializes a Structured Base structure.

        Parameters:
        - MarketObject: Market. Object containing market data (spot, vol, rates, dividends).
        - PricerObject: PricerBase. Object describing the pricer setup (method and settings).
        - maturity_date: datetime. Common maturity date for the certificate.
        """
        super().__init__(MarketObject, PricerObject)
        self.strategy_name = None
        self.products_params = []
        self.quantities = []