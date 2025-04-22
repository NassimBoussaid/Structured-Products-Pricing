import streamlit as st
from datetime import datetime
from Market import Market
from OptionAsian import OptionAsian
from PricerBS import PricerBS
from PricerMC import PricerMC
from PricerTree import PricerTree
from StrategyVanilla import StrategyVanilla

st.set_page_config(page_title="Asian Options Pricer")

st.markdown("<h3 style='color:#336699;'>Asian Options Pricer</h3>", unsafe_allow_html=True)

col_left, _ = st.columns([1, 2])

with col_left:
    cp_type = st.selectbox("Option Type:", ["Call", "Put"])

    stock_price = st.number_input("Stock price:", min_value=0.0, value=100.0)
    interest_rate = st.number_input("Interest rate:", min_value=0.0, value=0.02)
    dividend_yield = st.number_input("Dividend yield:", min_value=0.0, value=0.035)
    volatility = st.number_input("Volatility:", min_value=0.0, value=0.2)
    strike = st.number_input("Strike:", min_value=0.0, value=100.0)

    pricing_date = st.date_input("Pricing date:", value=datetime(2024, 1, 1))
    maturity_date = st.date_input("Maturity date:", value=datetime(2025, 1, 1))

    asian_freq = "Asianing Frequency:"


    pricer_choice = st.selectbox("Pricing model:", ["Monte Carlo", "Trinomial Tree"])

    if pricer_choice == "Monte Carlo":
        n_steps = st.number_input("Number of time steps:", min_value=1, value=100)
        n_draws = st.number_input("Number of paths:", min_value=1000, value=100000, step=1000)
        seed = st.number_input("Random seed:", min_value=0, value=1, step=1)
    elif pricer_choice == "Trinomial Tree":
        n_steps = st.number_input("Number of tree steps:", min_value=10, value=500, step=10)
        apply_pruning = st.radio("Apply pruning?", ["No", "Yes"], horizontal=True)
        pruning_mode = apply_pruning == "Yes"
        pruning_limit = st.number_input("Pruning limit:", min_value=0.0, value=0.001, step=0.001, format="%f")

    if st.button("Price it!"):
        market = Market(stock_price, volatility, interest_rate, "Continuous", dividend_yield, 0, maturity_date)
        option = OptionAsian(cp_type, strike, maturity_date, asian_freq)

        if pricer_choice == "Monte Carlo":
            pricer = PricerMC(pricing_date, n_steps, n_draws, seed)
        elif pricer_choice == "Trinomial Tree":
            pricer = PricerTree(pricing_date, n_steps, pruning_mode, pruning_limit)
        else:
            st.error("Modèle de pricing non reconnu.")
            st.stop()

        strategy = StrategyVanilla(market, option, pricer)
        price = strategy.price()

        st.success(f"Prix de l'option asiatique {cp_type} avec {pricer_choice} : {round(price, 6)}")
