from structured_products_pricing.Products.Options.OptionPricerManager import OptionPricerManager
from structured_products_pricing.Parameters.Option.OptionEuropean import OptionEuropean
from structured_products_pricing.Parameters.Pricer.PricerBase import PricerBase
from structured_products_pricing.Strategies.StrategyBase import StrategyBase
from structured_products_pricing.Parameters.Market import Market
from datetime import datetime

class StrategyCallSpread(StrategyBase):
    """
    Class to define a Call Spread strategy, extending from StrategyBase.

    A Call Spread combines:
    - Long one call at a lower strike (strike_1)
    - Short one call at a higher strike (strike_2)
    """
    def __init__(self, MarketObject: Market, PricerObject: PricerBase, strike_1: float, strike_2: float,
                 maturity_date: datetime):
        """
        Initializes a Call Spread strategy.

        Parameters:
        - MarketObject: Market. Object containing market data (spot, vol, rates, dividends).
        - PricerObject: PricerBase. Object describing the pricer setup (method and settings).
        - strike_1: float. Strike price of the long call (lower strike).
        - strike_2: float. Strike price of the short call (higher strike).
        - maturity_date: datetime. Common maturity date for both options.
        """
        super().__init__(MarketObject, PricerObject)
        self.strategy_name = "Call Spread"
        # Define the two European call options
        option_1 = OptionEuropean("Call", strike_1, maturity_date)
        option_2 = OptionEuropean("Call", strike_2, maturity_date)
        # Wrap each option with its pricer manager
        option_1_params = OptionPricerManager(self.Market, option_1, self.Pricer)
        option_2_params = OptionPricerManager(self.Market, option_2, self.Pricer)
        self.products_params = [option_1_params, option_2_params]
        self.quantities = [1, -1]