from sympy.physics.units import frequency
from structured_products_pricing.Parameters.Bond.BondZC import ZeroCouponBond
from structured_products_pricing.Parameters.Market import Market
from structured_products_pricing.Parameters.ModelParams import ModelParams
from structured_products_pricing.Parameters.Option.OptionBarrier import OptionBarrier
from structured_products_pricing.Parameters.Option.OptionEuropean import OptionEuropean
from structured_products_pricing.Parameters.Pricer.DiscountingPricer import DiscountingPricer
from structured_products_pricing.Parameters.Pricer.PricerBase import PricerBase
from structured_products_pricing.Products.Bond.RatePricerManager import RatePricerManager
from structured_products_pricing.Products.Options.OptionPricerMC import OptionPricerMC
from structured_products_pricing.Products.Options.OptionPricerManager import OptionPricerManager
from structured_products_pricing.Strategies.StrategiesOption.StrategyDigitalReplication import StrategyDigitalReplication
from structured_products_pricing.Strategies.StrategiesStructured.StrategyStructuredBase import StrategyStructuredBase
from structured_products_pricing.Utils.Calendar import Calendar
from datetime import datetime, timedelta


class StrategyStructuredAutocall(StrategyStructuredBase):
    def __init__(self, MarketObject: Market, PricerObject: PricerBase, strike: float, barrier_level: float, coupon_level: float,
                 coupon_frequency: str, maturity_date: datetime):
        super().__init__(MarketObject, PricerObject, maturity_date)
        self.strategy_name = "Autocall"
        # Adding PDI
        pdi = OptionBarrier("Put", strike, maturity_date, "in", "down", barrier_level, "American")
        pdi_params = OptionPricerManager(self.Market, pdi, self.Pricer)
        # Computing autocall probabilities from PDI (any options would be fine)
        autocall_params = pdi_params.compute_autocall_probabilities(coupon_frequency)
        pdi = OptionBarrier("Put", strike, self.Pricer.pricing_date + timedelta(days=365*autocall_params["duration"]), "in", "down", barrier_level, "American")
        pdi_params = OptionPricerManager(self.Market, pdi, self.Pricer)
        self.products_params += [pdi_params]
        self.quantities += [-1]
        # Adjust the ZC based on the estimated duration
        bond_zc = ZeroCouponBond(100, self.Pricer.pricing_date, self.Pricer.pricing_date + timedelta(days=365*autocall_params["duration"]))
        bond_zc_params = RatePricerManager(self.Market, bond_zc, DiscountingPricer(self.Pricer.pricing_date))
        self.products_params += [bond_zc_params]
        self.quantities += [1]
        # Computing digit strips
        coupon_gearing = coupon_level * 100
        for observation, probability in zip(autocall_params["observation_dates"], autocall_params["autocall_prob"]):
            digital = StrategyDigitalReplication(self.Market, self.Pricer, "Call", strike, 0.05, observation, coupon_gearing * probability)
            self.products_params += digital.products_params
            self.quantities += digital.quantities