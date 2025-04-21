from structured_products_pricing.Parameters.Market import Market
from structured_products_pricing.Parameters.Option.OptionEuropean import OptionEuropean
from structured_products_pricing.Parameters.Pricer.PricerBase import PricerBase
from structured_products_pricing.Products.Options.OptionPricerManager import OptionPricerManager
from structured_products_pricing.Strategies.StrategiesCertificates.StrategyCertificateBase import StrategyCertificateBase
from structured_products_pricing.Strategies.StrategiesOption.StrategyDigitalReplication import StrategyDigitalReplication
from datetime import datetime

class StrategyStructuredReverseConvertible(StrategyCertificateBase):
    def __init__(self, MarketObject: Market, PricerObject: PricerBase, strike: float, coupon_level: float,
                 maturity_date: datetime):
        super().__init__(MarketObject, PricerObject, maturity_date)
        self.strategy_name = "Reverse Convertible"
        option_1 = OptionEuropean("Put", strike, maturity_date)
        option_2 = StrategyDigitalReplication(self.Market, self.Pricer, "Call", 0, 0.01, maturity_date)
        option_1_params = OptionPricerManager(self.Market, option_1, self.Pricer)
        option_2_params = OptionPricerManager(self.Market, option_2, self.Pricer)
        coupon_gearing = coupon_level * 100
        self.products_params += [option_1_params, option_2_params]
        self.quantities += [-1, coupon_gearing]