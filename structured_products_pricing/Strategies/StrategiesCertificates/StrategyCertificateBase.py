from structured_products_pricing.Parameters.Market import Market
from structured_products_pricing.Parameters.Pricer.PricerBase import PricerBase
from structured_products_pricing.Strategies.StrategyBase import StrategyBase
from structured_products_pricing.Products.Options.OptionPricerManager import OptionPricerManager
from structured_products_pricing.Parameters.Option.OptionEuropean import OptionEuropean
from datetime import datetime

class StrategyCertificateBase(StrategyBase):
    def __init__(self, MarketObject: Market, PricerObject: PricerBase, maturity_date: datetime):
        super().__init__(MarketObject, PricerObject)
        self.strategy_name = None
        zero_strike_call = OptionEuropean("Call", 0, maturity_date)
        zero_strike_call_params = OptionPricerManager(self.Market, zero_strike_call, self.Pricer)
        self.products_params = [zero_strike_call_params]
        self.quantities = [1]