from structured_products_pricing.Parameters.Market import Market
from structured_products_pricing.Parameters.Pricer.PricerBase import PricerBase
from structured_products_pricing.Products.Options.OptionPricerManager import OptionPricerManager
from structured_products_pricing.Parameters.Option.OptionEuropean import OptionEuropean
from structured_products_pricing.Strategies.StrategiesCertificates.StrategyCertificateBase import StrategyCertificateBase
from datetime import datetime

class StrategyCertificateDiscount(StrategyCertificateBase):
    def __init__(self, MarketObject: Market, PricerObject: PricerBase, cap_level: float, maturity_date: datetime):
        super().__init__(MarketObject, PricerObject, maturity_date)
        self.strategy_name = "Discount"
        option = OptionEuropean("Call", cap_level, maturity_date)
        option_params = OptionPricerManager(self.Market, option, self.Pricer)
        self.products_params += [option_params]
        self.quantities += [-1]