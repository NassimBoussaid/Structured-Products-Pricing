from structured_products_pricing.Products.Options.OptionPricerManager import OptionPricerManager
from structured_products_pricing.Parameters.Option.OptionEuropean import OptionEuropean
from structured_products_pricing.Parameters.Pricer.PricerBase import PricerBase
from structured_products_pricing.Strategies.StrategyBase import StrategyBase
from structured_products_pricing.Parameters.Market import Market
from datetime import datetime

class StrategyCertificateBase(StrategyBase):
    """
    Base class to define the structure of certificates, extending from StrategyBase.
    """
    def __init__(self, MarketObject: Market, PricerObject: PricerBase, maturity_date: datetime):
        """
        Initializes a Certificate Base structure.

        Parameters:
        - MarketObject: Market. Object containing market data (spot, vol, rates, dividends).
        - PricerObject: PricerBase. Object describing the pricer setup (method and settings).
        - maturity_date: datetime. Common maturity date for the certificate.
        """
        super().__init__(MarketObject, PricerObject)
        self.strategy_name = None
        # Define a zero-strike European call (full participation in the asset)
        zero_strike_call = OptionEuropean("Call", 0, maturity_date)
        # Wrap the zero-strike call with its pricer manager
        zero_strike_call_params = OptionPricerManager(self.Market, zero_strike_call, self.Pricer)
        self.products_params = [zero_strike_call_params]
        self.quantities = [1]