from structured_products_pricing.Parameters.Market import Market
from structured_products_pricing.Parameters.Pricer.PricerBase import PricerBase
from structured_products_pricing.Strategies.StrategyBase import StrategyBase
from datetime import datetime
from structured_products_pricing.Strategies.StrategiesOption.StrategyCallSpread import StrategyCallSpread
from structured_products_pricing.Strategies.StrategiesOption.StrategyPutSpread import StrategyPutSpread

class StrategyDigitalReplication(StrategyBase):
    def __init__(self, MarketObject: Market, PricerObject: PricerBase, option_type: str, strike: float, epsilon: float,
                 maturity_date: datetime):
        super().__init__(MarketObject, PricerObject)
        self.strategy_name = "Digital Replication"
        if option_type == "Call":
            options = StrategyCallSpread(self.Market, self.Pricer, strike - epsilon, strike, maturity_date)
        elif option_type == "Put":
            options = StrategyPutSpread(self.Market, self.Pricer, strike - epsilon, strike, maturity_date)
        self.products_params = options.products_params
        digital_gearing = 1 / epsilon
        self.quantities = [digital_gearing, -digital_gearing]