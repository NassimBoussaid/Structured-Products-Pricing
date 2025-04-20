from Parameters.Market import Market
from Parameters.Option.OptionBase import OptionBase
from Parameters.Pricer.PricerBase import PricerBase
from Strategies.StrategyBase import StrategyBase
from Products.Options.OptionPricerManager import OptionPricerManager

class StrategyVanilla(StrategyBase):
    def __init__(self, MarketObject: Market, OptionObject: OptionBase, PricerObject: PricerBase):
        super().__init__(MarketObject, PricerObject)
        self.strategy_name = "Vanilla"
        option_params = OptionPricerManager(self.Market, OptionObject, self.Pricer)
        self.products_params = [option_params]
        self.quantities = [1]