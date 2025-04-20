from Parameters.Market import Market
from Parameters.Pricer.PricerBase import PricerBase
from Products.Options.OptionPricerManager import OptionPricerManager
from Parameters.Option.OptionEuropean import OptionEuropean
from Strategies.StrategiesCertificates.StrategyCertificateBase import StrategyCertificateBase
from datetime import datetime

class StrategyCertificateAirbag(StrategyCertificateBase):
    def __init__(self, MarketObject: Market, PricerObject: PricerBase, strike_1: float, strike_2: float,
                 maturity_date: datetime):
        super().__init__(MarketObject, PricerObject, maturity_date)
        self.strategy_name = "Airbag"
        option_1 = OptionEuropean("Call", 0, maturity_date)
        option_2 = OptionEuropean("Call", strike_1, maturity_date)
        option_3 = OptionEuropean("Call", strike_2, maturity_date)
        option_1_params = OptionPricerManager(self.Market, option_1, self.Pricer)
        option_2_params = OptionPricerManager(self.Market, option_2, self.Pricer)
        option_3_params = OptionPricerManager(self.Market, option_3, self.Pricer)
        airbag_leverage = strike_2 / strike_1
        self.products_params = [option_1_params, option_2_params, option_3_params]
        self.quantities = [airbag_leverage, -airbag_leverage, 1]