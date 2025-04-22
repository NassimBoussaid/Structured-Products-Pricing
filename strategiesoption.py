import streamlit as st
from datetime import datetime
from Market import Market
from PricerBS import PricerBS
from PricerMC import PricerMC
from PricerTree import PricerTree
from StrategyCallSpread import StrategyCallSpread
from StrategyPutSpread import StrategyPutSpread
from StrategyStraddle import StrategyStraddle
from StrategyStrangle import StrategyStrangle
from StrategyButterflySpread import StrategyButterflySpread
from StrategyCondorSpread import StrategyCondorSpread

st.set_page_config(page_title="Option Strategies Pricer")

st.markdown("<h3 style='color:#336699;'>Option Strategies Pricer</h3>", unsafe_allow_html=True)

col_left, _ = st.columns([1, 2])

with col_left:
    strategy = st.selectbox("Option Strategy Type:", [
        "Call Spread", "Put Spread", "Straddle", "Strangle", "Butterfly Spread", "Condor Spread"])

    stock_price = st.number_input("Stock price:", min_value=0.0, value=100.0)
    interest_rate = st.number_input("Interest rate:", min_value=0.0, value=0.02)
    dividend_yield = st.number_input("Dividend yield:", min_value=0.0, value=0.035)
    volatility = st.number_input("Volatility:", min_value=0.0, value=0.2)

    pricing_date = st.date_input("Pricing date:", value=datetime(2024, 1, 1)).strftime("%Y-%m-%d")
    dividend_date = st.date_input("Dividend date:", value=datetime(2024, 6, 1)).strftime("%Y-%m-%d")
    maturity_date = st.date_input("Maturity date:", value=datetime(2025, 1, 1)).strftime("%Y-%m-%d")
    pricing_date_obj = datetime.strptime(pricing_date, "%Y-%m-%d")
    dividend_date_obj = datetime.strptime(dividend_date, "%Y-%m-%d")
    maturity_date_obj = datetime.strptime(maturity_date, "%Y-%m-%d")

    pricer_choice = st.selectbox("Pricing model:", ["Black-Scholes", "Monte Carlo", "Trinomial Tree"])

    if pricer_choice == "Monte Carlo":
        n_steps = st.number_input("Number of time steps:", min_value=1, value=100)
        n_draws = st.number_input("Number of paths:", min_value=1000, value=100000, step=1000)
        seed = st.number_input("Random seed:", min_value=0, value=1, step=1)
    elif pricer_choice == "Trinomial Tree":
        n_steps = st.number_input("Number of tree steps:", min_value=10, value=500, step=10)
        apply_pruning = st.radio("Apply pruning?", ["No", "Yes"], horizontal=True)
        pruning_mode = apply_pruning == "Yes"
        pruning_limit = st.number_input("Pruning limit:", min_value=0.0, value=0.001, step=0.001, format="%f")

    strategy_map = {
        "Call Spread": 2,
        "Put Spread": 2,
        "Straddle": 1,
        "Strangle": 2,
        "Butterfly Spread": 3,
        "Condor Spread": 4
    }
    n_options = strategy_map.get(strategy, 2)

    st.markdown("**Options' strikes :**")
    option_strikes = []

    for i in range(n_options):
        strike = st.number_input(f"Strike {i+1}", value=100.0 + 10 * i, key=f"strike_{i}")
        option_strikes.append(strike)

    if st.button("Price this strategy!"):
        market = Market(stock_price, volatility, interest_rate, "Continuous", dividend_yield, 0, dividend_date_obj)

        if pricer_choice == "Black-Scholes":
            pricer = PricerBS(pricing_date_obj )
        elif pricer_choice == "Monte Carlo":
            pricer = PricerMC(pricing_date_obj , n_steps, n_draws, seed)
        elif pricer_choice == "Trinomial Tree":
            pricer = PricerTree(pricing_date_obj , n_steps, pruning_mode, pruning_limit)
        else:
            st.error("Modèle de pricing non reconnu.")
            st.stop()

        if strategy == "Call Spread":
            strat = StrategyCallSpread(market, pricer, option_strikes[0], option_strikes[1], maturity_date_obj)
        elif strategy == "Put Spread":
            strat = StrategyPutSpread(market, pricer, option_strikes[0], option_strikes[1], maturity_date_obj)
        elif strategy == "Straddle":
            strat = StrategyStraddle(market, pricer, option_strikes[0], maturity_date_obj)
        elif strategy == "Strangle":
            strat = StrategyStrangle(market, pricer, option_strikes[0], option_strikes[1], maturity_date_obj)
        elif strategy == "Butterfly Spread":
            strat = StrategyButterflySpread(market, pricer, option_strikes[0], option_strikes[1], option_strikes[2],
                                            maturity_date_obj)
        elif strategy == "Condor Spread":
            strat = StrategyCondorSpread(market, pricer, option_strikes[0], option_strikes[1], option_strikes[2],
                                         option_strikes[3], maturity_date_obj)

            st.error("Stratégie non reconnue.")
            st.stop()

        price = strat.price()
        st.success(f"Prix de la stratégie '{strategy}' avec {pricer_choice} : {round(price, 6)}")
