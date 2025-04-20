from Parameters.Market import Market
from Parameters.Pricer.PricerBase import PricerBase
from Products.Options.OptionPricerManager import OptionPricerManager
from Parameters.Option.OptionEuropean import OptionEuropean
from Strategies.StrategiesCertificates.StrategyCertificateBase import StrategyCertificateBase
from datetime import datetime

class StrategyCertificateDiscount(StrategyCertificateBase):
    def __init__(self, MarketObject: Market, PricerObject: PricerBase, cap_level: float, maturity_date: datetime):
        super().__init__(MarketObject, PricerObject, maturity_date)
        self.strategy_name = "Discount"
        option = OptionEuropean("Call", cap_level, maturity_date)
        option_params = OptionPricerManager(self.Market, option, self.Pricer)
        self.products_params += [option_params]
        self.quantities += [-1]