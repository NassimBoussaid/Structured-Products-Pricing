from structured_products_pricing.Strategies.StrategiesOption.StrategyOptionVanilla import StrategyOptionVanilla
from structured_products_pricing.Parameters.Option.OptionEuropean import OptionEuropean
from structured_products_pricing.Parameters.Pricer.PricerBS import PricerBS
from structured_products_pricing.Parameters.Market import Market
from datetime import datetime
import pytest

@pytest.fixture
def setup_pricer_client():
    """
    Fixture to create a basic market, pricer, and strategy setup.
    """
    market = Market(
        underlying_price=100,
        volatility=0.20,
        rate_mode="constant",
        interest_rate=0.02,
        div_mode="Continuous",
        dividend_rate=0.035,
        dividend_discrete=0.00,
        dividend_date=datetime(2025, 6, 1)
    )

    pricer_bs = PricerBS(
        pricing_date=datetime(2025, 1, 1)
    )

    strategy = StrategyOptionVanilla(
        MarketObject=market,
        OptionObject=OptionEuropean("Call", 100, datetime(2026, 1, 1)),
        PricerObject=pricer_bs,
    )

    return strategy

def test_compute_price_exact(setup_pricer_client):
    """
    Test that the computed price matches an expected value.
    """
    strategy = setup_pricer_client
    computed_price = strategy.price()

    expected_price = 7.04
    tolerance = 0.1

    assert abs(computed_price - expected_price) < tolerance, \
        f"❌ Price mismatch! Expected ~{expected_price}, got {computed_price:.6f}"

def test_compute_greeks_exact(setup_pricer_client):
    """
    Test that the computed greeks match an expected value.
    """
    strategy = setup_pricer_client
    computed_greeks = strategy.greeks()

    expected_greeks = [0.492, 0.019, 0.385, -0.012, 0.422]
    tolerance = 0.1

    for greek, expected_greek in zip(computed_greeks, expected_greeks):
        assert abs(greek - expected_greek) < tolerance, \
            f"❌ Greek mismatch! Expected ~{expected_greek}, got {greek:.6f}"

def test_greeks_output_shape(setup_pricer_client):
    """
    Test that greeks return arrays of the correct shape.
    """
    strategy = setup_pricer_client
    greeks = strategy.greeks()
    expected_length = 5

    assert len(greeks) == expected_length, \
        f"❌ Greeks length mismatch! Expected ~{expected_length}, got {greeks.length:.6f}"

def test_greeks_values_type(setup_pricer_client):
    """
    Test that Greek values are floats.
    """
    strategy = setup_pricer_client
    greeks = strategy.greeks()

    for greek in greeks:
        assert isinstance(greek, (float, int)), f"❌ {greek} is not a number, got {type(greek)}."

def test_market_properties():
    """
    Test that Market initializes with correct properties.
    """
    market = Market(100, 0.2, 0.02, "Continuous", 0.035, 0, datetime(2024, 6, 1))

    assert market.und_price == 100, "❌ Spot price mismatch."
    assert market.vol == 0.2, "❌ Volatility mismatch."

def test_pricer_properties():
    """
    Test PricerBS initializes with the correct pricing date.
    """
    pricing_date = datetime(2025, 1, 1)
    pricer = PricerBS(pricing_date=pricing_date)

    assert pricer.pricing_date == pricing_date, "❌ Pricing date mismatch."

def test_option_properties():
    """
    Test that OptionEuropean initializes correctly.
    """
    maturity_date = datetime(2026, 1, 1)
    option = OptionEuropean("Call", 100, maturity_date)

    assert option.option_type == "Call", "❌ Option type mismatch."
    assert option.strike == 100, "❌ Strike mismatch."
    assert option.maturity_date == maturity_date, "❌ Maturity mismatch."