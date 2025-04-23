from structured_products_pricing.Parameters.Option.OptionEuropean import OptionEuropean
from structured_products_pricing.Parameters.Market import Market
from structured_products_pricing.Parameters.Pricer.PricerMC import PricerMC
from datetime import datetime

from structured_products_pricing.Parameters.Pricer.PricerTree import PricerTree
from structured_products_pricing.Strategies.StrategiesOption.StrategyDigitalReplication import StrategyDigitalReplication
from structured_products_pricing.Strategies.StrategiesStructured.StrategyStructuredBarrierReverseConvertible import \
    StrategyStructuredBarrierReverseConvertible
from structured_products_pricing.Strategies.StrategyVanilla import StrategyVanilla
from structured_products_pricing.Strategies.StrategiesStructured.StrategyStructuredReverseConvertible import StrategyStructuredReverseConvertible
from structured_products_pricing.Volatility.ImpliedVolatility import ImpliedVolatility

Market_Info = Market(238, 1.01250954638158, 0.02, "Continuous",
                     0, 0, datetime(2024, 6, 1))
#Pricer_Info = PricerMC(datetime(2024, 1, 1), 100, 200000, 1)
Pricer_Info = PricerTree(datetime(2024, 10, 11), 500, "False", 1e-7)
#a = StrategyStructuredReverseConvertible(Market_Info, Pricer_Info, 100, 0.105, datetime(2025, 1, 1))
#a = StrategyStructuredBarrierReverseConvertible(Market_Info, Pricer_Info, 100, 80, 0.084, datetime(2025, 1, 1))
Option_Info = OptionEuropean("Call", 220, datetime(2024, 10, 18))
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

implied_vol = ImpliedVolatility()
implied_vol.initialize_surface(Market_Info, Option_Info, Pricer_Info)
x = implied_vol.get_volatility(173,200)

