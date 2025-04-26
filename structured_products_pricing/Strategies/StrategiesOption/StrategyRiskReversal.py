from structured_products_pricing.Products.Options.OptionPricerManager import OptionPricerManager
from structured_products_pricing.Parameters.Option.OptionEuropean import OptionEuropean
from structured_products_pricing.Parameters.Pricer.PricerBase import PricerBase
from structured_products_pricing.Strategies.StrategyBase import StrategyBase
from structured_products_pricing.Parameters.Market import Market
from datetime import datetime

class StrategyRiskReversal(StrategyBase):
    """
    Class to define a Risk Reversal strategy, extending from StrategyBase.

    A Risk Reversal typically involves:
    - Short one put at a lower strike (strike_1)
    - Long one call at a higher strike (strike_2)
    """
    def __init__(self, MarketObject: Market, PricerObject: PricerBase, strike_1: float, strike_2: float,
                 maturity_date: datetime):
        """
        Initializes a Risk Reversal strategy.

        Parameters:
        - MarketObject: Market. Object containing market data (spot, vol, rates, dividends).
        - PricerObject: PricerBase. Object describing the pricer setup (method and settings).
        - strike_1: float. Strike price of the short put (lower strike).
        - strike_2: float. Strike price of the long call (higher strike).
        - maturity_date: datetime. Common maturity date for both options.
        """
        super().__init__(MarketObject, PricerObject)
        self.strategy_name = "Risk Reversal"
        # Define the put and call options
        option_1 = OptionEuropean("Put", strike_1, maturity_date)
        option_2 = OptionEuropean("Call", strike_2, maturity_date)
        # Wrap each option with its pricer manager
        option_1_params = OptionPricerManager(self.Market, option_1, self.Pricer)
        option_2_params = OptionPricerManager(self.Market, option_2, self.Pricer)
        self.products_params = [option_1_params, option_2_params]
        self.quantities = [-1, 1]