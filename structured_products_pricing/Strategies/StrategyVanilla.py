from structured_products_pricing.Parameters.Market import Market
from structured_products_pricing.Parameters.Option.OptionBase import OptionBase
from structured_products_pricing.Parameters.Pricer.PricerBase import PricerBase
from structured_products_pricing.Strategies.StrategyBase import StrategyBase
from structured_products_pricing.Products.Options.OptionPricerManager import OptionPricerManager

class StrategyVanilla(StrategyBase):
    def __init__(self, MarketObject: Market, OptionObject: OptionBase, PricerObject: PricerBase):
        super().__init__(MarketObject, PricerObject)
        self.strategy_name = "Vanilla"
        option_params = OptionPricerManager(self.Market, OptionObject, self.Pricer)
        self.products_params = [option_params]
        self.quantities = [1]