from structured_products_pricing.Products.Options.OptionPricerManager import OptionPricerManager
from structured_products_pricing.Parameters.Option.OptionEuropean import OptionEuropean
from structured_products_pricing.Parameters.Pricer.PricerBase import PricerBase
from structured_products_pricing.Strategies.StrategyBase import StrategyBase
from structured_products_pricing.Parameters.Market import Market
from datetime import datetime

class StrategyCondorSpread(StrategyBase):
    """
    Class to define a Condor Spread strategy, extending from StrategyBase.

    A Condor Spread combines four call options:
    - Long one call at the lowest strike (strike_1)
    - Short one call at the second strike (strike_2)
    - Short one call at the third strike (strike_3)
    - Long one call at the highest strike (strike_4)
    """
    def __init__(self, MarketObject: Market, PricerObject: PricerBase, strike_1: float, strike_2: float,
                 strike_3, strike_4, maturity_date: datetime):
        """
        Initializes a Condor Spread strategy.

        Parameters:
        - MarketObject: Market. Object containing market data (spot, vol, rates, dividends).
        - PricerObject: PricerBase. Object describing the pricer setup (method and settings).
        - strike_1: float. Strike price of the first long call (lowest strike).
        - strike_2: float. Strike price of the first short call.
        - strike_3: float. Strike price of the second short call.
        - strike_4: float. Strike price of the second long call (highest strike).
        - maturity_date: datetime. Common maturity date for all options.
        """
        super().__init__(MarketObject, PricerObject)
        self.strategy_name = "Condor Spread"
        # Define the four European call options
        option_1 = OptionEuropean("Call", strike_1, maturity_date)
        option_2 = OptionEuropean("Call", strike_2, maturity_date)
        option_3 = OptionEuropean("Call", strike_3, maturity_date)
        option_4 = OptionEuropean("Call", strike_4, maturity_date)
        # Wrap each option with its pricer manager
        option_1_params = OptionPricerManager(self.Market, option_1, self.Pricer)
        option_2_params = OptionPricerManager(self.Market, option_2, self.Pricer)
        option_3_params = OptionPricerManager(self.Market, option_3, self.Pricer)
        option_4_params = OptionPricerManager(self.Market, option_4, self.Pricer)
        self.products_params = [option_1_params, option_2_params, option_3_params, option_4_params]
        self.quantities = [1, -1, -1, 1]