from structured_products_pricing.Parameters.Market import Market
from structured_products_pricing.Parameters.Pricer.PricerBase import PricerBase
from structured_products_pricing.Strategies.StrategyBase import StrategyBase
from structured_products_pricing.Products.Options.OptionPricerManager import OptionPricerManager
from structured_products_pricing.Parameters.Option.OptionEuropean import OptionEuropean
from datetime import datetime

class StrategyCondorSpread(StrategyBase):
    def __init__(self, MarketObject: Market, PricerObject: PricerBase, strike_1: float, strike_2: float,
                 strike_3, strike_4, maturity_date: datetime):
        super().__init__(MarketObject, PricerObject)
        self.strategy_name = "Condor Spread"
        option_1 = OptionEuropean("Call", strike_1, maturity_date)
        option_2 = OptionEuropean("Call", strike_2, maturity_date)
        option_3 = OptionEuropean("Call", strike_3, maturity_date)
        option_4 = OptionEuropean("Call", strike_4, maturity_date)
        option_1_params = OptionPricerManager(self.Market, option_1, self.Pricer)
        option_2_params = OptionPricerManager(self.Market, option_2, self.Pricer)
        option_3_params = OptionPricerManager(self.Market, option_3, self.Pricer)
        option_4_params = OptionPricerManager(self.Market, option_4, self.Pricer)
        self.products_params = [option_1_params, option_2_params, option_3_params, option_4_params]
        self.quantities = [1, -1, -1, 1]