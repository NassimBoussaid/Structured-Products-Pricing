from structured_products_pricing.Strategies.StrategiesCertificates.StrategyCertificateBase import StrategyCertificateBase
from structured_products_pricing.Products.Options.OptionPricerManager import OptionPricerManager
from structured_products_pricing.Parameters.Option.OptionEuropean import OptionEuropean
from structured_products_pricing.Parameters.Pricer.PricerBase import PricerBase
from structured_products_pricing.Parameters.Market import Market
from datetime import datetime

class StrategyCertificateDiscount(StrategyCertificateBase):
    """
    Class to define a Discount Certificate strategy, extending from StrategyCertificateBase.
    """
    def __init__(self, MarketObject: Market, PricerObject: PricerBase, cap_level: float, maturity_date: datetime):
        """
        Initializes a Discount Certificate strategy.

        Parameters:
        - MarketObject: Market. Object containing market data (spot, vol, rates, dividends).
        - PricerObject: PricerBase. Object describing the pricer setup (method and settings).
        - cap_level: float. Strike price of the cap (short call).
        - maturity_date: datetime. Common maturity date for the product.
        """
        super().__init__(MarketObject, PricerObject, maturity_date)
        self.strategy_name = "Discount"
        # Define the European call option to cap the upside
        option = OptionEuropean("Call", cap_level, maturity_date)
        # Wrap the call option with its pricer manager
        option_params = OptionPricerManager(self.Market, option, self.Pricer)
        self.products_params += [option_params]
        self.quantities += [-1]