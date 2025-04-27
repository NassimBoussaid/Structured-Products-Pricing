from structured_products_pricing.Strategies.StrategiesOption.StrategyDigitalReplication import StrategyDigitalReplication
from structured_products_pricing.Strategies.StrategiesStructured.StrategyStructuredBase import StrategyStructuredBase
from structured_products_pricing.Products.Options.OptionPricerManager import OptionPricerManager
from structured_products_pricing.Products.Bond.RatePricerManager import RatePricerManager
from structured_products_pricing.Parameters.Option.OptionBarrier import OptionBarrier
from structured_products_pricing.Parameters.Pricer.PricerBase import PricerBase
from structured_products_pricing.Parameters.Bond.BondZC import ZeroCouponBond
from structured_products_pricing.Parameters.Market import Market
from datetime import datetime, timedelta

class StrategyStructuredAutocall(StrategyStructuredBase):
    """
    Class to define an Autocallable Structured Product strategy, extending from StrategyStructuredBase.

    An Autocall combines:
    - A capital protection or partial protection component (PDI),
    - A bond component,
    - A set of coupon payments triggered at observation dates based on barrier conditions.
    """
    def __init__(self, MarketObject: Market, PricerObject: PricerBase, strike_pdi: float, barrier_pdi: float, barrier_autocall: float,
                 barrier_coupon: float, coupon_level: float, coupon_frequency: str, maturity_date: datetime):
        """
        Initializes an Autocallable strategy.

        Parameters:
        - MarketObject: Market. Object containing market data (spot, vol, rates, dividends).
        - PricerObject: PricerBase. Object describing the pricer setup (method and settings).
        - strike_pdi: float. Strike of the put down-and-in (PDI) option.
        - barrier_pdi: float. Barrier level for the PDI.
        - barrier_autocall: float. Barrier triggering autocall events.
        - barrier_coupon: float. Barrier level for triggering coupon payments.
        - coupon_level: float. Nominal level of each coupon payment.
        - coupon_frequency: str. Frequency of coupon observations ("monthly", "quarterly", etc.).
        - maturity_date: datetime. Final maturity date if no autocall occurs.
        """
        super().__init__(MarketObject, PricerObject, maturity_date)
        self.strategy_name = "Autocall"
        # Add the PDI (Put Down-and-In)
        pdi = OptionBarrier("Put", strike_pdi, maturity_date, "in", "down", barrier_pdi, "American")
        pdi_params = OptionPricerManager(self.Market, pdi, self.Pricer)
        # Estimate the autocall probabilities
        autocall_params = pdi_params.compute_autocall_probabilities(barrier_autocall, coupon_frequency)
        # Adjust PDI maturity to expected autocall duration
        pdi = OptionBarrier("Put", strike_pdi, self.Pricer.pricing_date + timedelta(days=365*autocall_params["duration"]), "in", "down", barrier_pdi, "American")
        pdi_params = OptionPricerManager(self.Market, pdi, self.Pricer)
        self.products_params = [pdi_params]
        self.quantities = [-1/strike_pdi * 100]
        # Add a Zero-Coupon Bond to match the expected autocall date
        bond_zc = ZeroCouponBond(100, self.Pricer.pricing_date, self.Pricer.pricing_date + timedelta(days=365*autocall_params["duration"]))
        bond_zc_params = RatePricerManager(self.Market, bond_zc, self.Pricer.pricing_date)
        self.products_params += [bond_zc_params]
        self.quantities += [1]
        # Add the digital coupons at each observation date
        coupon_gearing = coupon_level * self.Market.und_price
        for observation, probability in zip(autocall_params["observation_dates"], autocall_params["autocall_prob"]):
            digital = StrategyDigitalReplication(self.Market, self.Pricer, "Call", barrier_coupon, 0.05, observation, coupon_gearing * probability)
            self.products_params += digital.products_params
            self.quantities += [x/self.Market.und_price * 100 for x in digital.quantities]