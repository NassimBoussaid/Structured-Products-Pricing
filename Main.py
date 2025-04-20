from Parameters.ModelParams import ModelParams
from Parameters.Option.OptionEuropean import OptionEuropean
from Parameters.Option.OptionDigital import OptionDigital
from Parameters.Option.OptionBarrier import OptionBarrier
from Parameters.Option.OptionAsian import OptionAsian
from Parameters.Market import Market
from Parameters.Pricer.PricerMC import PricerMC
from Parameters.Pricer.PricerBS import PricerBS
from datetime import datetime
from Strategies.StrategyVanilla import StrategyVanilla
from Strategies.StrategiesOption.StrategyCallSpread import StrategyCallSpread
from Strategies.StrategiesOption.StrategyRiskReversal import StrategyRiskReversal
from Strategies.StrategiesOption.StrategyButterflySpread import StrategyButterflySpread
from Strategies.StrategiesOption.StrategyCondorSpread import StrategyCondorSpread
from Strategies.StrategiesOption.StrategyStraddle import StrategyStraddle
from Strategies.StrategiesOption.StrategyStrangle import StrategyStrangle
from Strategies.StrategiesOption.StrategyPutSpread import StrategyPutSpread

Market_Info = Market(100, 0.2, 0.02, "Continuous",
                     0, 0, datetime(2024, 6, 1))
Pricer_Info = PricerMC(datetime(2024, 1, 1), 100, 100000, 1)
#Pricer_Info = PricerBS(datetime(2024, 1, 1))
#a = StrategyRiskReversal(Market_Info, Pricer_Info, 80, 120, datetime(2025, 1, 1))
a = StrategyPutSpread(Market_Info, Pricer_Info, 80, 100, datetime(2025, 1, 1))
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