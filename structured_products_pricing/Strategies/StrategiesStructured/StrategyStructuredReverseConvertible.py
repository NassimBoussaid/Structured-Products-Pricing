from structured_products_pricing.Strategies.StrategiesStructured.StrategyStructuredBase import StrategyStructuredBase
from structured_products_pricing.Products.Options.OptionPricerManager import OptionPricerManager
from structured_products_pricing.Parameters.Pricer.DiscountingPricer import DiscountingPricer
from structured_products_pricing.Products.Bond.RatePricerManager import RatePricerManager
from structured_products_pricing.Parameters.Option.OptionEuropean import OptionEuropean
from structured_products_pricing.Parameters.Pricer.PricerBase import PricerBase
from structured_products_pricing.Parameters.Bond.BondZC import ZeroCouponBond
from structured_products_pricing.Parameters.Market import Market
from datetime import datetime

class StrategyStructuredReverseConvertible(StrategyStructuredBase):
    """
    Class to define a Reverse Convertible strategy, extending from StrategyStructuredBase.
    """
    def __init__(self, MarketObject: Market, PricerObject: PricerBase, strike: float, coupon_level: float,
                 maturity_date: datetime):
        """
        Initializes a Reverse Convertible strategy.

        Parameters:
        - MarketObject: Market. Object containing market data (spot, vol, rates, dividends).
        - PricerObject: PricerBase. Object describing the pricer setup (method and settings).
        - strike: float. Strike price of the short put option.
        - coupon_level: float. Annualized coupon level (as a percentage of notional).
        - maturity_date: datetime. Final maturity date of the product.
        """
        super().__init__(MarketObject, PricerObject, maturity_date)
        self.strategy_name = "Reverse Convertible"
        # Define the zero-coupon bond paying back nominal plus coupon
        bond_zc = ZeroCouponBond(100 * (1 + coupon_level), self.Pricer.pricing_date, maturity_date)
        bond_zc_params = RatePricerManager(self.Market, bond_zc, DiscountingPricer(self.Pricer.pricing_date))
        # Define the put option
        option = OptionEuropean("Put", strike, maturity_date)
        option_params = OptionPricerManager(self.Market, option, self.Pricer)
        self.products_params += [bond_zc_params, option_params]
        self.quantities += [1, -1]