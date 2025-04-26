from structured_products_pricing.Products.Options.OptionPricerManager import OptionPricerManager
from structured_products_pricing.Parameters.Option.OptionEuropean import OptionEuropean
from structured_products_pricing.Parameters.Pricer.PricerBase import PricerBase
from structured_products_pricing.Strategies.StrategyBase import StrategyBase
from structured_products_pricing.Parameters.Market import Market
from datetime import datetime

class StrategyButterflySpread(StrategyBase):
    """
    Class to define a Butterfly Spread strategy, extending from StrategyBase.

    A Butterfly Spread combines three call options:
    - Long one call at lower strike (strike_1)
    - Short two calls at middle strike (strike_2)
    - Long one call at higher strike (strike_3)
    """
    def __init__(self, MarketObject: Market, PricerObject: PricerBase, strike_1: float, strike_2: float,
                 strike_3, maturity_date: datetime):
        """
        Initializes a Butterfly Spread strategy.

        Parameters:
        - MarketObject: Market. Object containing market data (spot, vol, rates, dividends).
        - PricerObject: PricerBase. Object describing the pricer setup (method and settings).
        - strike_1: float. Strike price of the first long call (lower strike).
        - strike_2: float. Strike price of the two short calls (middle strike).
        - strike_3: float. Strike price of the second long call (higher strike).
        - maturity_date: datetime. Common maturity date for all options.
        """
        super().__init__(MarketObject, PricerObject)
        self.strategy_name = "Butterfly Spread"
        # Define the three European call options
        option_1 = OptionEuropean("Call", strike_1, maturity_date)
        option_2 = OptionEuropean("Call", strike_2, maturity_date)
        option_3 = OptionEuropean("Call", strike_3, maturity_date)
        # Wrap each option with its pricer manager
        option_1_params = OptionPricerManager(self.Market, option_1, self.Pricer)
        option_2_params = OptionPricerManager(self.Market, option_2, self.Pricer)
        option_3_params = OptionPricerManager(self.Market, option_3, self.Pricer)
        self.products_params = [option_1_params, option_2_params, option_3_params]
        self.quantities = [1, -2, 1]