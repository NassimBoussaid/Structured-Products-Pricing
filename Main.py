from structured_products_pricing.Parameters.ModelParams import ModelParams
from structured_products_pricing.Parameters.Option.OptionEuropean import OptionEuropean
from structured_products_pricing.Parameters.Market import Market
from structured_products_pricing.Parameters.Pricer.DiscountingPricer import DiscountingPricer
from datetime import datetime

from structured_products_pricing.Parameters.Pricer.PricerMC import PricerMC
from structured_products_pricing.Parameters.Pricer.PricerTree import PricerTree
from structured_products_pricing.Parameters.Bond.BondZC import ZeroCouponBond
from structured_products_pricing.Products.Bond.RatePricerManager import RatePricerManager
from structured_products_pricing.Strategies.StrategiesStructured.StrategyStructuredAutocall import \
    StrategyStructuredAutocall
from structured_products_pricing.Utils.Calendar import Calendar

calendar = Calendar(start_date=datetime(2024, 1, 1), end_date=datetime(2024, 1, 1))
Market_Info = Market(100, 0.2, 0.02, "Continuous",
                     0.035, 0, datetime(2024, 6, 1))
Pricer_Info = PricerMC(datetime(2024, 1, 1), 100, 40000, 1)
#Pricer_Info = PricerTree(datetime(2024, 10, 11), 500, "False", 1e-7)
#a = StrategyStructuredReverseConvertible(Market_Info, Pricer_Info, 100, 0.105, datetime(2025, 1, 1))
#a = StrategyStructuredBarrierReverseConvertible(Market_Info, Pricer_Info, 100, 80, 0.084, datetime(2025, 1, 1))
#Option_Info = OptionEuropean("Call", 220, datetime(2024, 10, 18))
#Bond_Info = ZeroCouponBond(1000000, datetime(2024, 1, 1), datetime(2026, 1, 1))
#Pricer_Info = DiscountingPricer(datetime(2025, 1, 1))
#cc = RatePricerManager(Market_Info, Bond_Info, Pricer_Info)
#print(cc.compute_price())
#Option_Info = OptionBarrier("Put", 100, datetime(2025, 1, 1), "out", "down", 80, "American")
#a = StrategyDigitalReplication(Market_Info, Pricer_Info, "Call", 0, 0.01, datetime(2025, 1, 1), 10.5)
#a = StrategyVanilla(Market_Info, Option_Info, Pricer_Info)
#a = StrategyCertificateDiscount(Market_Info, Pricer_Info, 115, datetime(2025, 1, 1))
#a = StrategyCertificateAirbag(Market_Info, Pricer_Info, 80, 120, datetime(2025, 1, 1))
a = StrategyStructuredAutocall(Market_Info, Pricer_Info, 100, 80, 0.05, "yearly",
                               datetime(2034, 1, 1))
price = a.price()
print(price)
#Option_Info = OptionBarrier("Call", 100, datetime(2025, 1, 1), "in", "up", 120, "European")
#Params_Info = ModelParams(Market_Info, Option_Info, Pricer_Info)
#a = StrategyVanilla([Params_Info], [1])
#price = a.price()
#print(price)
#MC = MonteCarlo(Params_Info)
#price = MC.price_vector()
#print(price)

#implied_vol = ImpliedVolatility()
#implied_vol.initialize_surface(Market_Info, Option_Info, Pricer_Info)
#x = implied_vol.get_volatility(173,200)
'''
# Test Curve Nico
rate_curve = RateCurve(0.01, 0.01, 0.01, 1)
rate_curve.compute_yield_curve()
print(rate_curve.get_yield(0.33))

##### Test Taux #####
pricer = RatePricer(pricing_date=datetime(2025, 1, 1), day_count='act/365.25')

# Zero Coupon Bond
zc = ZeroCouponBond(notional=1, issue_date='2025-01-01', maturity_date='2027-01-01')
price_zcb = pricer.compute_price(zc, Market_Info)
print(f"Prix Zero Coupon Bond: {price_zcb:.4f}")

# Fixed Rate Bond
bond = FixedRateBond(
    notional=1,
    issue_date='2025-01-01',
    maturity_date='2027-01-01',
    coupon_rate=0.05,
    frequency='yearly',
    day_count='30/360'
)
price_frb = pricer.compute_price(bond, Market_Info, clean=False)
print(f"Prix Fixed Rate Bond: {price_frb:.4f}")

# Floating Rate Bond
flb = FloatingRateBond(
    notional=1,
    issue_date='2025-01-01',
    maturity_date='2027-01-01',
    index_curve=rate_curve,
    spread=0.002,  # 20 bps de marge
    frequency='yearly',
    day_count='30/360'
)
price = pricer.compute_price(flb, Market_Info)
print(f"Prix Floating Rate Bond : {price:.4f}")

# Swap
swap = InterestRateSwap(
    notional=1,
    issue_date='2025-01-01',
    maturity_date='2027-01-01',
    fixed_rate=0.02,  # 2% fixe
    index_curve=rate_curve,  # patte flottante
    spread=0.0,  # pas de spread
    frequency='yearly',
    day_count='act/365.25'
)
price = pricer.compute_price(swap, Market_Info)
print(f"Prix Interest Rate Swap : {price:.4f}")
'''