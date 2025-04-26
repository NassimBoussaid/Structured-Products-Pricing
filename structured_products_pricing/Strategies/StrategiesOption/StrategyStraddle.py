from structured_products_pricing.Products.Options.OptionPricerManager import OptionPricerManager
from structured_products_pricing.Parameters.Option.OptionEuropean import OptionEuropean
from structured_products_pricing.Parameters.Pricer.PricerBase import PricerBase
from structured_products_pricing.Strategies.StrategyBase import StrategyBase
from structured_products_pricing.Parameters.Market import Market
from datetime import datetime

class StrategyStraddle(StrategyBase):
    """
    Class to define a Straddle strategy, extending from StrategyBase.

    A Straddle involves:
    - Long one call and one put at the same strike and same maturity,
    """
    def __init__(self, MarketObject: Market, PricerObject: PricerBase, strike: float, maturity_date: datetime):
        """
        Initializes a Straddle strategy.

        Parameters:
        - MarketObject: Market. Object containing market data (spot, vol, rates, dividends).
        - PricerObject: PricerBase. Object describing the pricer setup (method and settings).
        - strike: float. Strike price for both the call and the put.
        - maturity_date: datetime. Common maturity date for both options.
        """
        super().__init__(MarketObject, PricerObject)
        self.strategy_name = "Straddle"
        # Define the European call and put options with the same strike
        option_1 = OptionEuropean("Call", strike, maturity_date)
        option_2 = OptionEuropean("Put", strike, maturity_date)
        # Wrap each option with its pricer manager
        option_1_params = OptionPricerManager(self.Market, option_1, self.Pricer)
        option_2_params = OptionPricerManager(self.Market, option_2, self.Pricer)
        self.products_params = [option_1_params, option_2_params]
        self.quantities = [1, 1]