from structured_products_pricing.Strategies.StrategiesCertificates.StrategyCertificateBase import StrategyCertificateBase
from structured_products_pricing.Products.Options.OptionPricerManager import OptionPricerManager
from structured_products_pricing.Parameters.Option.OptionEuropean import OptionEuropean
from structured_products_pricing.Parameters.Pricer.PricerBase import PricerBase
from structured_products_pricing.Parameters.Market import Market
from datetime import datetime

class StrategyCertificateAirbag(StrategyCertificateBase):
    """
    Class to define an Airbag Certificate strategy, extending from StrategyCertificateBase.
    """
    def __init__(self, MarketObject: Market, PricerObject: PricerBase, strike_1: float, strike_2: float,
                 maturity_date: datetime):
        """
        Initializes an Airbag Certificate strategy.

        Parameters:
        - MarketObject: Market. Object containing market data (spot, vol, rates, dividends).
        - PricerObject: PricerBase. Object describing the pricer setup (method and settings).
        - strike_1: float. Strike price of the first call option (lower strike for leveraged participation).
        - strike_2: float. Strike price of the second call option (cap level).
        - maturity_date: datetime. Common maturity date for all options.
        """
        super().__init__(MarketObject, PricerObject, maturity_date)
        self.strategy_name = "Airbag"
        # Define the three European call options
        option_1 = OptionEuropean("Call", 0, maturity_date)
        option_2 = OptionEuropean("Call", strike_1, maturity_date)
        option_3 = OptionEuropean("Call", strike_2, maturity_date)
        # Wrap each option with its pricer manager
        option_1_params = OptionPricerManager(self.Market, option_1, self.Pricer)
        option_2_params = OptionPricerManager(self.Market, option_2, self.Pricer)
        option_3_params = OptionPricerManager(self.Market, option_3, self.Pricer)
        # Calculate the airbag leverage
        airbag_leverage = strike_2 / strike_1
        self.products_params = [option_1_params, option_2_params, option_3_params]
        self.quantities = [airbag_leverage, -airbag_leverage, 1]