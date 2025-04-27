from structured_products_pricing.Parameters.Bond.BondFixedRate import FixedRateBond
from structured_products_pricing.Parameters.Bond.BondFloatingRate import FloatingRateBond
from structured_products_pricing.Parameters.Bond.InterestRateSwap import InterestRateSwap
from structured_products_pricing.Parameters.ModelParams import ModelParams
from structured_products_pricing.Parameters.Option.OptionEuropean import OptionEuropean
from structured_products_pricing.Parameters.Market import Market
from structured_products_pricing.Parameters.Pricer.DiscountingPricer import DiscountingPricer
from datetime import datetime
from structured_products_pricing.Parameters.Option.OptionBarrier import OptionBarrier
from structured_products_pricing.Parameters.Pricer.PricerMC import PricerMC
from structured_products_pricing.Parameters.Pricer.PricerTree import PricerTree
from structured_products_pricing.Parameters.Bond.BondZC import ZeroCouponBond
from structured_products_pricing.Products.Bond.RatePricerManager import RatePricerManager
from structured_products_pricing.Products.Options.OptionPricerManager import OptionPricerManager
from structured_products_pricing.Rate.RateCurve import RateCurve
from structured_products_pricing.Rate.RateStochastic import RateStochastic
from structured_products_pricing.Strategies.StrategiesOption.StrategyOptionVanilla import StrategyOptionVanilla
from structured_products_pricing.Strategies.StrategiesStructured.StrategyStructuredAutocall import \
    StrategyStructuredAutocall
from structured_products_pricing.Strategies.StrategiesStructured.StrategyStructuredBarrierReverseConvertible import \
    StrategyStructuredBarrierReverseConvertible
from structured_products_pricing.Strategies.StrategiesStructured.StrategyStructuredReverseConvertible import \
    StrategyStructuredReverseConvertible
from structured_products_pricing.Utils.Calendar import Calendar
from structured_products_pricing.Strategies.StrategiesOption.StrategyDigitalReplication import \
    StrategyDigitalReplication
from structured_products_pricing.Volatility.ImpliedVolatility import ImpliedVolatility

# calendar = Calendar(start_date=datetime(2024, 1, 1), end_date=datetime(2024, 1, 1))
Market_Info = Market(100, 0.2,"constant", 0.02, "Continuous",
                     0.035, 0, datetime(2024, 6, 1))
Pricer_Info = PricerMC(datetime(2024, 1, 1), 10, 10000, 1)
# Pricer_Info = PricerTree(datetime(2024, 10, 11), 500, "False", 1e-7)
# a = StrategyStructuredReverseConvertible(Market_Info, Pricer_Info, 100, 0.105, datetime(2025, 1, 1))
# a = StrategyStructuredBarrierReverseConvertible(Market_Info, Pricer_Info, 100, 80, 0.084, datetime(2025, 1, 1))
Option_Info = OptionEuropean("Call", 100, datetime(2026, 1, 1))
# Bond_Info = ZeroCouponBond(1000000, datetime(2024, 1, 1), datetime(2025, 1, 1))
# Pricer_Info = DiscountingPricer(datetime(2025, 1, 1))
# cc = RatePricerManager(Market_Info, Bond_Info, Pricer_Info)
# print(cc.compute_price())
# Option_Info = OptionBarrier("Put", 100, datetime(2025, 1, 1), "in", "down", 80, "American")
# b = OptionPricerManager(Market_Info, Option_Info, Pricer_Info)
# a = StrategyDigitalReplication(Market_Info, Pricer_Info, "Call", 100, 0.2, datetime(2025, 1, 1), 1)
# a = StrategyOptionVanilla(Market_Info, Option_Info, Pricer_Info)
# a = StrategyCertificateDiscount(Market_Info, Pricer_Info, 115, datetime(2025, 1, 1))
# a = StrategyCertificateAirbag(Market_Info, Pricer_Info, 80, 120, datetime(2025, 1, 1))
# a = StrategyStructuredAutocall(Market_Info, Pricer_Info, 100, 80, 100, 100, 0.01, "monthly", datetime(2025, 1, 1))
# a = StrategyStructuredBarrierReverseConvertible(Market_Info, Pricer_Info, 80, 80, 0.1, datetime(2025, 1, 1))
# price = a.greeks_over_spot_range(True)
# print(price)
# import matplotlib.pyplot as plt
# Plot Delta
# plt.plot(price["Spot"], price["Payoff"])
# plt.xlabel("Spot Price")
# plt.ylabel("Price")
# plt.title("Delta vs Spot Price")
# plt.grid(True)
# plt.show()

# price = b.compute_price()
# print(price)
# Option_Info = OptionBarrier("Call", 100, datetime(2025, 1, 1), "in", "up", 120, "European")
# Params_Info = ModelParams(Market_Info, Option_Info, Pricer_Info)
# a = StrategyVanilla([Params_Info], [1])
# price = a.price()
# print(price)
# MC = MonteCarlo(Params_Info)
# price = MC.price_vector()
# print(price)
"""
implied_vol = ImpliedVolatility()
implied_vol.initialize_surface(Market_Info, Option_Info, Pricer_Info)
x = implied_vol.get_volatility(173, 200)

rate_curve = RateCurve(0.01, 0.01, 0.01, 1)
rate_curve.compute_yield_curve()
print(rate_curve.get_yield(0.33))


# Test Curve Nico
rate_curve = RateCurve(0.01, 0.01, 0.01, 1)
rate_curve.compute_yield_curve()
print(rate_curve.get_yield(0.33))
"""
##### Test Taux #####


# Zero Coupon Bond
zc = ZeroCouponBond(notional=1, issue_date='2025-01-01', maturity_date='2027-01-01')
pricer = RatePricerManager(MarketObject=Market_Info,
                           BondObject=zc,
                           pricing_date=datetime(2025, 1, 1))
print(f"Prix Zero Coupon Bond: {pricer.compute_price():.4f}")

# Fixed Rate Bond
bond = FixedRateBond(
    notional=1,
    issue_date='2025-01-01',
    maturity_date='2027-01-01',
    coupon_rate=0.05,
    frequency='yearly',
    day_count='30/360'
)
pricer = RatePricerManager(MarketObject=Market_Info,
                           BondObject=bond,
                           pricing_date=datetime(2025, 1, 1))
print(f"Prix Fixed Rate Bond: {pricer.compute_price():.4f}")

# Floating Rate Bond
flb = FloatingRateBond(
    notional=1,
    issue_date='2025-01-01',
    maturity_date='2027-01-01',
    spread=0.002,  # 20 bps de marge
    frequency='yearly',
    day_count='30/360'
)
pricer = RatePricerManager(MarketObject=Market_Info,
                           BondObject=flb,
                           pricing_date=datetime(2025, 1, 1))
print(f"Prix Floating Rate Bond: {pricer.compute_price():.4f}")

# Swap
swap = InterestRateSwap(
    notional=1,
    issue_date='2025-01-01',
    maturity_date='2027-01-01',
    fixed_rate=0.02,  # 2% fixe
    spread=0.0,  # pas de spread
    frequency='yearly',
    day_count='act/365.25'
)
pricer = RatePricerManager(MarketObject=Market_Info,
                           BondObject=swap,
                           pricing_date=datetime(2025, 1, 1))
print(f"Prix Swap: {pricer.compute_price():.4f}")

