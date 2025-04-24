from structured_products_pricing.Parameters.Bond.BondZC import ZeroCouponBond
from structured_products_pricing.Parameters.Market import Market
from structured_products_pricing.Parameters.Pricer.DiscountingPricer import DiscountingPricer
from structured_products_pricing.Parameters.Pricer.PricerBase import PricerBase
from structured_products_pricing.Products.Bond.RatePricerManager import RatePricerManager
from structured_products_pricing.Strategies.StrategyBase import StrategyBase
from datetime import datetime

class StrategyStructuredBase(StrategyBase):
    def __init__(self, MarketObject: Market, PricerObject: PricerBase, maturity_date: datetime):
        super().__init__(MarketObject, PricerObject)
        self.strategy_name = None
        self.products_params = []
        self.quantities = []