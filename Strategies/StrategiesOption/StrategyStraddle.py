from Parameters.Market import Market
from Parameters.Pricer.PricerBase import PricerBase
from Strategies.StrategyBase import StrategyBase
from Products.Options.OptionPricerManager import OptionPricerManager
from Parameters.Option.OptionEuropean import OptionEuropean
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