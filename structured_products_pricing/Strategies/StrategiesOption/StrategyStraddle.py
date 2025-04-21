from structured_products_pricing.Parameters.Market import Market
from structured_products_pricing.Parameters.Pricer.PricerBase import PricerBase
from structured_products_pricing.Strategies.StrategyBase import StrategyBase
from structured_products_pricing.Products.Options.OptionPricerManager import OptionPricerManager
from structured_products_pricing.Parameters.Option.OptionEuropean import OptionEuropean
from datetime import datetime

class StrategyStraddle(StrategyBase):
    def __init__(self, MarketObject: Market, PricerObject: PricerBase, strike: float, maturity_date: datetime):
        super().__init__(MarketObject, PricerObject)
        self.strategy_name = "Straddle"
        option_1 = OptionEuropean("Call", strike, maturity_date)
        option_2 = OptionEuropean("Put", strike, maturity_date)
        option_1_params = OptionPricerManager(self.Market, option_1, self.Pricer)
        option_2_params = OptionPricerManager(self.Market, option_2, self.Pricer)
        self.products_params = [option_1_params, option_2_params]
        self.quantities = [1, 1]