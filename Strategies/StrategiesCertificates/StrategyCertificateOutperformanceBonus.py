from Parameters.Market import Market
from Parameters.Option.OptionEuropean import OptionEuropean
from Parameters.Pricer.PricerBase import PricerBase
from Products.Options.OptionPricerManager import OptionPricerManager
from Parameters.Option.OptionBarrier import OptionBarrier
from Strategies.StrategiesCertificates.StrategyCertificateBase import StrategyCertificateBase
from datetime import datetime

class StrategyCertificateOutperformanceBonus(StrategyCertificateBase):
    def __init__(self, MarketObject: Market, PricerObject: PricerBase, bonus_level: float, barrier_level: float,
                 upside_participation: float, maturity_date: datetime):
        super().__init__(MarketObject, PricerObject, maturity_date)
        self.strategy_name = "Outperformance Bonus"
        option_1 = OptionBarrier("Put", bonus_level, maturity_date, "out", "down", barrier_level, "American")
        option_2 = OptionEuropean("Call", bonus_level, maturity_date)
        option_1_params = OptionPricerManager(self.Market, option_1, self.Pricer)
        option_2_params = OptionPricerManager(self.Market, option_2, self.Pricer)
        self.products_params += [option_1_params, option_2_params]
        self.quantities += [1, (upside_participation - 1)]