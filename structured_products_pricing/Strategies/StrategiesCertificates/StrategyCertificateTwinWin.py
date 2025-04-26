from structured_products_pricing.Strategies.StrategiesCertificates.StrategyCertificateBase import StrategyCertificateBase
from structured_products_pricing.Products.Options.OptionPricerManager import OptionPricerManager
from structured_products_pricing.Parameters.Option.OptionBarrier import OptionBarrier
from structured_products_pricing.Parameters.Pricer.PricerBase import PricerBase
from structured_products_pricing.Parameters.Market import Market
from datetime import datetime

class StrategyCertificateTwinWin(StrategyCertificateBase):
    """
    Class to define a Twin Win Certificate strategy, extending from StrategyCertificateBase.
    """
    def __init__(self, MarketObject: Market, PricerObject: PricerBase, strike: float, barrier_level: float,
                 maturity_date: datetime):
        """
        Initializes a Twin Win Certificate strategy.

        Parameters:
        - MarketObject: Market. Object containing market data (spot, vol, rates, dividends).
        - PricerObject: PricerBase. Object describing the pricer setup (method and settings).
        - strike: float. Strike price used for the barrier put.
        - barrier_level: float. Barrier level for protection.
        - maturity_date: datetime. Common maturity date for the product.
        """
        super().__init__(MarketObject, PricerObject, maturity_date)
        self.strategy_name = "Twin Win"
        # Define the barrier put option used to capture both upside and downside
        option = OptionBarrier("Put", strike, maturity_date, "out", "down", barrier_level, "American")
        # Wrap the barrier option with its pricer manager
        option_params = OptionPricerManager(self.Market, option, self.Pricer)
        self.products_params += [option_params]
        self.quantities += [2]