from structured_products_pricing.Parameters.Option.OptionEuropean import OptionEuropean
from structured_products_pricing.Parameters.Market import Market
from structured_products_pricing.Parameters.Pricer.PricerMC import PricerMC
from datetime import datetime

from structured_products_pricing.Rate.RateCurve import RateCurve
from structured_products_pricing.Strategies.StrategiesOption.StrategyDigitalReplication import StrategyDigitalReplication
from structured_products_pricing.Strategies.StrategiesStructured.StrategyStructuredBarrierReverseConvertible import \
    StrategyStructuredBarrierReverseConvertible
from structured_products_pricing.Strategies.StrategyVanilla import StrategyVanilla
from structured_products_pricing.Strategies.StrategiesStructured.StrategyStructuredReverseConvertible import StrategyStructuredReverseConvertible

Market_Info = Market(100, 0.2, 0.02, "Continuous",
                     0.035, 0, datetime(2024, 6, 1))
Pricer_Info = PricerMC(datetime(2024, 1, 1), 100, 200000, 1)
#a = StrategyStructuredReverseConvertible(Market_Info, Pricer_Info, 100, 0.105, datetime(2025, 1, 1))
a = StrategyStructuredBarrierReverseConvertible(Market_Info, Pricer_Info, 100, 80, 0.084, datetime(2025, 1, 1))
#Option_Info = OptionEuropean("Call", 100, datetime(2025, 1, 1))
#Option_Info = OptionBarrier("Put", 100, datetime(2025, 1, 1), "out", "down", 80, "American")
#a = StrategyDigitalReplication(Market_Info, Pricer_Info, "Call", 0, 0.01, datetime(2025, 1, 1), 10.5)
#a = StrategyVanilla(Market_Info, Option_Info, Pricer_Info)
#a = StrategyCertificateDiscount(Market_Info, Pricer_Info, 115, datetime(2025, 1, 1))
#a = StrategyCertificateAirbag(Market_Info, Pricer_Info, 80, 120, datetime(2025, 1, 1))
#price = a.price()
#print(price)
#Option_Info = OptionBarrier("Call", 100, datetime(2025, 1, 1), "in", "up", 120, "European")
#Params_Info = ModelParams(Market_Info, Option_Info, Pricer_Info)
#a = StrategyVanilla([Params_Info], [1])
#price = a.price()
#print(price)
#MC = MonteCarlo(Params_Info)
#price = MC.price_vector()
#print(price)

rate_curve = RateCurve(0.01, 0.01, 0.01, 1)
rate_curve.compute_yield_curve()
print(rate_curve.get_yield(0.33))