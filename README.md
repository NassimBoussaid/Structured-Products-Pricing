# Structured-Products-Pricing
![Python](https://img.shields.io/badge/Python-%E2%89%A53.9-blue)
![Poetry](https://img.shields.io/badge/Package%20Manager-Poetry-5C2D91)
![License](https://img.shields.io/badge/License-MIT-green)

## Overview

This repository contains a modular, extensible framework designed for the pricing and risk analysis of financial products.  
It is based on an object-oriented architecture, enabling easy addition of new products and models.  
The system supports pricing vanilla options, certificates, bonds, and complex structured products.

---

## Key Features

- **Flexible Market Setup**:
  - Handle continuous and discrete dividends.
  - Set customizable interest rates and volatility parameters.

- **Multi-Product Pricing**:
  - European Calls and Puts.
  - American Options.
  - Asian Options.
  - Digital (Binary) Options.
  - Barrier Options (Knock-In/Knock-Out).
  - Certificates (Discount, Airbag, Bonus, Capped Bonus, Outperformance Bonus, Twin Win).
  - Static Strategies (Call Spread, Put Spread, Straddle, Strangle, Butterfly, Condor, Risk Reversal, Strap, Strip).
  - Structured Strategies (Reverse Convertible, Barrier Reverse Convertible, Autocallable Notes).

- **Risk Metrics**:
  - Full computation of Greeks: Delta, Gamma, Vega, Theta, and Rho.
  - Estimation of autocall probabilities.

- **Model Calibration**:
  - Calibrate volatilities and risk-free rates directly from market data.

- **Interactive Dashboard**:
  - Streamlit-based interface for real-time pricing and visualization.
  - Analyze prices, payoffs, greeks via an intuitive web app.

---

## Structure

```
Structured-Product-Pricing/
├── .github/                         # GitHub-related files (e.g., workflows, actions)
├── images/                          # Documentation images (e.g., for README or Streamlit)
├── structured_products_pricing/     # Main source code package
│   ├── Parameters/                  # Financial product definitions and input parameters
│   ├── Products/                    # Product managers for pricing
│   │   ├── Bond/                    # Pricer for fixed income products
│   │   ├── Options/                 # Option pricing engines
│   ├── Rate/                        # Interest rate curve models (flat, curve, stochastic)
│   ├── Strategies/                  # Pricing strategies and structured products
│   │   ├── StrategiesCertificates/  # Certificate products (discount, bonus, airbag, etc.)
│   │   ├── StrategiesOption/        # Static option strategies (spread, condor, strangle...)
│   │   ├── StrategiesStructured/    # Structured notes (reverse convertible, autocallable)
│   │   ├── StrategyBase.py          # Abstract base class for all strategies
│   ├── Utils/                       # Utility scripts
│   ├── Volatility/                  # Volatility calibration tools
│   ├── Demo.py                      # Demonstration script
│   ├── App.py                       # Streamlit Interface script
│   ├── Views/                       # Individual Streamlit interface of each product
│   │   ├── Asian_option/             # Streamlit view for Asian options
│   │   ├── Barrier_option/           # Streamlit view for Barrier options
│   │   ├── Certificate/              # Streamlit view for Certificates (Discount, Bonus, Airbag, etc.)
│   │   ├── Classic_option.py         # Base class for classic vanilla options
│   │   ├── Strategies_option.py      # Base class for static option strategies (spreads, condor, strangle...)
│   │   ├── Structured_product.py     # Base class for structured products (reverse convertible, autocallable, etc.)
├── tests/                           # Unit and functional test scripts (pytest framework)
├── LICENSE                          # License information
├── poetry.lock                      # Dependency lock file
├── pyproject.toml                   # Project dependencies and configuration
├── README.md                        # Project documentation
```

## Installation

Clone the repository:

```bash
git clone https://github.com/NassimBoussaid/Structured-Products-Pricing.git
cd Structured-Products-Pricing
```

Dependencies are managed with Poetry:

```bash
pip install poetry
poetry install
poetry check
poetry shell
```

---

## Usage

### Running Pricing Scripts

Launch a simple pricing script by configuring a Market, a Pricer, and a Strategy:

```python
from structured_products_pricing.Strategies.StrategiesOption.StrategyOptionVanilla import StrategyOptionVanilla
from structured_products_pricing.Parameters.Option.OptionEuropean import OptionEuropean
from structured_products_pricing.Parameters.Pricer.PricerMC import PricerMC
from structured_products_pricing.Parameters.Market import Market
from datetime import datetime

# Initialize
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
pricer = PricerMC(
            pricing_date=datetime(2025, 1, 1),
            nb_steps=50,
            nb_draws=100000,
            seed=1
        )
option = OptionEuropean(
            option_type="Call",
            strike=100,
            maturity_date=datetime(2026, 1, 1)
        )
strategy = StrategyOptionVanilla(market, option, pricer)

# Compute price and Greeks
print("Price:", strategy.price())
print("Greeks:", strategy.greeks())
```

---

### Running Unit Tests

Ensure your setup is correct by running the tests:

```bash
poetry run pytest
```

This will test key components like pricers, strategies, and market setups.

---

### Running the Streamlit Interface

To launch the Streamlit dashboard:

```bash
poetry run streamlit run structured_products_pricing/app.py
```

The web app allows you to:
- Input custom market parameters and product configurations.
- Compute and visualize prices and greeks.
- Perform stress tests over spot ranges.

---

## Examples of Supported Products

| Product Type                          | Description                                                                                                        |
|----------------------------------------|--------------------------------------------------------------------------------------------------------------------|
| European Call / Put                   | Vanilla options priced using Black-Scholes closed-form, Monte Carlo simulation, and trinomial tree models.         |
| American Options                      | Early-exercise options priced using Longstaff-Schwartz or tree-based methods.                                      |
| Asian Options                         | Average price options priced via Monte Carlo simulations.                                                          |
| Digital (Binary) Options              | Options with fixed payout; supported both with Monte Carlo simulations and replication strategies.                 |
| Barrier Options (In/Out, Up/Down)      | Options activated or deactivated based on barrier events, with pricing via Monte Carlo.                            |
| Discount Certificates                 | Structured products offering reduced entry price but capped upside potential.                                      |
| Bonus and Capped Bonus Certificates   | Products combining upside participation with a guaranteed bonus if no barrier breach occurs.                       |
| Airbag Certificates                   | Structured certificates providing downside protection up to a certain point.                                       |
| Outperformance Bonus Certificates     | Products combining upside leverage above the performance of the underlying asset.                                  |
| Twin Win Certificates                 | Instruments providing positive payout for both upside and downside movements up to a certain point.                |
| Call Spreads / Put Spreads             | Static option strategies composed of buying and selling options at different strikes.                              |
| Straddle / Strangle                   | Static strategies betting on volatility using simultaneous Call and Put purchases.                                 |
| Butterfly / Condor Spreads             | Range-bound option strategies using multiple strikes.                                                              |
| Risk Reversal                         | Strategy combining a bought Call and a sold Put (or vice versa) to gain directional exposure.                      |
| Strap / Strip                         | Directional volatility plays using uneven numbers of Calls and Puts.                                               |
| Reverse Convertible Notes             | Structured products offering high yields with the risk of equity conversion at maturity.                           |
| Barrier Reverse Convertible Notes     | Same as RCNs but with additional barrier protection features.                                                      |
| Autocallable Notes                    | Structured products featuring periodic redemption opportunities if the underlying stays above predefined barriers. |
| Zero Coupon Bonds (ZC)                | Fixed-income instruments paying a single amount at maturity, without periodic coupons.                             |

---

## Authors

- Nassim BOUSSAID
- Nicolas COUTURAUD
- Karthy MOUROUGAYA
- Hugo SOULIER

Supervised by M. Laurent Davoust

---

## License

This project is licensed under the MIT License.
