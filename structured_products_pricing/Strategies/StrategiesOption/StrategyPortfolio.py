from structured_products_pricing.Parameters.Market import Market
from structured_products_pricing.Parameters.Pricer.PricerBase import PricerBase
from structured_products_pricing.Strategies.StrategyBase import StrategyBase
from structured_products_pricing.Products.Options.OptionPricerManager import OptionPricerManager
from structured_products_pricing.Parameters.Option.OptionEuropean import OptionEuropean
from datetime import datetime
from typing import List

class StrategyPortfolio(StrategyBase):
    def __init__(self, MarketObject: Market, PricerObject: PricerBase, option_types: List[str], strikes: List[float],
                 option_quantities: List[float], maturity_date: datetime):
        super().__init__(MarketObject, PricerObject)
        self.strategy_name = "Portfolio"
        self.products_params = []
        self.quantities = []
        for option_type, strike, quantity in zip(option_types, strikes, option_quantities):
            option = OptionEuropean(option_type, strike, maturity_date)
            option_params = OptionPricerManager(self.Market, option, self.Pricer)
            self.products_params += [option_params]
            self.quantities += [quantity]