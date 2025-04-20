from Parameters.Market import Market
from Parameters.Pricer.PricerBase import PricerBase
from Strategies.StrategyBase import StrategyBase
from Products.Options.OptionPricerManager import OptionPricerManager
from Parameters.Option.OptionEuropean import OptionEuropean
from datetime import datetime

class StrategyPutSpread(StrategyBase):
    def __init__(self, MarketObject: Market, PricerObject: PricerBase, strike_1: float, strike_2: float,
                 maturity_date: datetime):
        super().__init__(MarketObject, PricerObject)
        self.strategy_name = "Put Spread"
        option_1 = OptionEuropean("Put", strike_1, maturity_date)
        option_2 = OptionEuropean("Put", strike_2, maturity_date)
        option_1_params = OptionPricerManager(self.Market, option_1, self.Pricer)
        option_2_params = OptionPricerManager(self.Market, option_2, self.Pricer)
        self.products_params = [option_1_params, option_2_params]
        self.quantities = [-1, 1]