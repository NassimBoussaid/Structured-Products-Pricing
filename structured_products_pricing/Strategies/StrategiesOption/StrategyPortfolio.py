from structured_products_pricing.Products.Options.OptionPricerManager import OptionPricerManager
from structured_products_pricing.Parameters.Option.OptionEuropean import OptionEuropean
from structured_products_pricing.Parameters.Pricer.PricerBase import PricerBase
from structured_products_pricing.Strategies.StrategyBase import StrategyBase
from structured_products_pricing.Parameters.Market import Market
from datetime import datetime
from typing import List

class StrategyPortfolio(StrategyBase):
    """
    Class to define a general Portfolio strategy, extending from StrategyBase.

    This strategy allows combining multiple vanilla options (calls or puts) with arbitrary strikes
    and quantities into a single customizable portfolio.
    """
    def __init__(self, MarketObject: Market, PricerObject: PricerBase, option_types: List[str], strikes: List[float],
                 option_quantities: List[float], maturity_date: datetime):
        """
        Initializes a Portfolio strategy.

        Parameters:
        - MarketObject: Market. Object containing market data (spot, vol, rates, dividends).
        - PricerObject: PricerBase. Object describing the pricer setup (method and settings).
        - option_types: List[str]. List of option types ("Call" or "Put") for each option.
        - strikes: List[float]. List of strike prices corresponding to each option.
        - option_quantities: List[float]. List of quantities for each option (positive for long, negative for short).
        - maturity_date: datetime. Common maturity date for all options.
        """
        super().__init__(MarketObject, PricerObject)
        self.strategy_name = "Portfolio"
        # Initialize empty lists to store products and quantities
        self.products_params = []
        self.quantities = []
        # Loop over each option specification and build the portfolio
        for option_type, strike, quantity in zip(option_types, strikes, option_quantities):
            # Create the European option
            option = OptionEuropean(option_type, strike, maturity_date)
            # Wrap the option with its pricer
            option_params = OptionPricerManager(self.Market, option, self.Pricer)
            self.products_params += [option_params]
            self.quantities += [quantity]