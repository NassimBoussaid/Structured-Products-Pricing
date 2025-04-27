from structured_products_pricing.Strategies.StrategiesStructured.StrategyStructuredBarrierReverseConvertible import StrategyStructuredBarrierReverseConvertible
from structured_products_pricing.Strategies.StrategiesStructured.StrategyStructuredAutocall import StrategyStructuredAutocall
from structured_products_pricing.Strategies.StrategiesOption.StrategyDigitalReplication import StrategyDigitalReplication
from structured_products_pricing.Strategies.StrategiesOption.StrategyOptionVanilla import StrategyOptionVanilla
from structured_products_pricing.Strategies.StrategiesOption.StrategyStraddle import StrategyStraddle
from structured_products_pricing.Parameters.Option.OptionAmerican import OptionAmerican
from structured_products_pricing.Parameters.Option.OptionBarrier import OptionBarrier
from structured_products_pricing.Parameters.Option.OptionEuropean import OptionEuropean
from structured_products_pricing.Parameters.Pricer.PricerTree import PricerTree
from structured_products_pricing.Parameters.Pricer.PricerBS import PricerBS
from structured_products_pricing.Parameters.Pricer.PricerMC import PricerMC
from structured_products_pricing.Parameters.Market import Market
from datetime import datetime

class PricerClient:
    """
    A client to set up market, pricer, and strategy for structured product pricing.
    """
    def __init__(self):
        self.market = None
        self.pricer_mc = None
        self.pricer_tree = None
        self.pricer_bs = None
        self.strategy = None

    def setup_market(self):
        print("Setting up the Market...")
        self.market = Market(
            underlying_price=100,
            volatility=0.20,
            rate_mode="constant",
            interest_rate=0.02,
            div_mode="Continuous",
            dividend_rate=0.035,
            dividend_discrete=0.00,
            dividend_date=datetime(2025, 6, 1)
        )
        print("✅ Market ready.\n")

    def setup_pricer_mc(self):
        print("Setting up the Pricer (Monte Carlo)...")
        self.pricer_mc = PricerMC(
            pricing_date=datetime(2025, 1, 1),
            nb_steps=50,
            nb_draws=100000,
            seed=1
        )
        print("✅ Pricer ready.\n")

    def setup_pricer_tree(self):
        print("Setting up the Pricer (Tree)...")
        self.pricer_tree = PricerTree(
            pricing_date=datetime(2025, 1, 1),
            nb_steps=10,
            pruning_mode=True,
            pruning_limit=1e-7
        )
        print("✅ Pricer ready.\n")

    def setup_pricer_bs(self):
        print("Setting up the Pricer (Black Scholes)...")
        self.pricer_bs = PricerBS(
            pricing_date=datetime(2025, 1, 1)
        )
        print("✅ Pricer ready.\n")

    def setup_strategy_1(self):
        self.strategy = StrategyOptionVanilla(
            MarketObject=self.market,
            OptionObject=OptionEuropean("Call", 100, datetime(2026, 1, 1)),
            PricerObject=self.pricer_mc,
        )

    def setup_strategy_2(self):
        self.strategy = StrategyOptionVanilla(
            MarketObject=self.market,
            OptionObject=OptionBarrier("Put", 100, datetime(2026, 1, 1), "in",
                                       "down", 80, "American"),
            PricerObject=self.pricer_mc,
        )

    def setup_strategy_3(self):
        self.strategy = StrategyOptionVanilla(
            MarketObject=self.market,
            OptionObject=OptionAmerican("Call", 100, datetime(2026, 1, 1),
                                        "Classic", 2),
            PricerObject=self.pricer_mc,
        )

    def setup_strategy_4(self):
        self.strategy = StrategyDigitalReplication(
            MarketObject=self.market,
            PricerObject=self.pricer_mc,
            option_type="Call",
            strike=100,
            epsilon=0.5,
            maturity_date=datetime(2026, 1, 1),
            coupon_level=1
        )

    def setup_strategy_5(self):
        self.strategy = StrategyStraddle(
            MarketObject=self.market,
            PricerObject=self.pricer_mc,
            strike=100,
            maturity_date=datetime(2026, 1, 1)
        )

    def setup_strategy_6(self):
        self.strategy = StrategyStructuredBarrierReverseConvertible(
            MarketObject=self.market,
            PricerObject=self.pricer_mc,
            strike=100,
            barrier_level=80,
            coupon_level=0.1,
            maturity_date=datetime(2026, 1, 1)
        )

    def setup_strategy_7(self):
        self.strategy = StrategyStructuredAutocall(
            MarketObject=self.market,
            PricerObject=self.pricer_mc,
            strike_pdi=100,
            barrier_pdi=80,
            barrier_autocall=100,
            barrier_coupon=100,
            coupon_level=0.01,
            coupon_frequency="monthly",
            maturity_date=datetime(2026, 1, 1)
        )

    def run_pricing(self):
        print(f"🚀Computing price for {self.strategy.strategy_name}...")
        price = self.strategy.price()
        print(f"✅ Computed price: {price:.4f}\n")

    def run_greeks_analysis(self):
        print(f"📈 Generating greeks analysis for {self.strategy.strategy_name}...")
        greeks = self.strategy.greeks()
        print(f"✅ Computed greeks (Delta, Gamma, Vega, Theta, Rho): {greeks}\n")

def main():
    client = PricerClient()
    client.setup_market()
    client.setup_pricer_mc()
    client.setup_strategy_1()
    client.run_pricing()
    client.run_greeks_analysis()
    client.setup_strategy_2()
    client.run_pricing()
    client.setup_strategy_3()
    client.run_pricing()
    client.setup_strategy_4()
    client.run_pricing()
    client.setup_strategy_5()
    client.run_pricing()
    client.setup_strategy_6()
    client.run_pricing()
    client.setup_strategy_7()
    client.run_pricing()

if __name__ == "__main__":
    main()