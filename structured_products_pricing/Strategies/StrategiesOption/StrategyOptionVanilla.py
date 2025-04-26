from structured_products_pricing.Products.Options.OptionPricerManager import OptionPricerManager
from structured_products_pricing.Parameters.Option.OptionBase import OptionBase
from structured_products_pricing.Parameters.Pricer.PricerBase import PricerBase
from structured_products_pricing.Strategies.StrategyBase import StrategyBase
from structured_products_pricing.Parameters.Market import Market

class StrategyOptionVanilla(StrategyBase):
    """
    Class to define a Vanilla strategy (single vanilla option) extending from StrategyBase.
    """
    def __init__(self, MarketObject: Market, OptionObject: OptionBase, PricerObject: PricerBase):
        """
        Initializes a Vanilla strategy.

        Parameters:
        - MarketObject: Market. Object containing market data (spot, vol, rates, dividends).
        - OptionObject: OptionBase. Object describing the option to be priced.
        - PricerObject: PricerBase. Object describing the pricer setup (method and settings).
        """
        super().__init__(MarketObject, PricerObject)
        # Wrap the single option into an OptionPricerManager
        option_params = OptionPricerManager(self.Market, OptionObject, self.Pricer)
        self.strategy_name = OptionObject.option_name
        self.products_params = [option_params]
        self.quantities = [1]