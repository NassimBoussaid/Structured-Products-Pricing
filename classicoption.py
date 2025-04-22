import streamlit as st
from datetime import datetime
from Market import Market
from OptionEuropean import OptionEuropean
from OptionDigital import OptionDigital
from OptionAmerican import OptionAmerican
from PricerBS import PricerBS
from PricerMC import PricerMC
from PricerTree import PricerTree
from StrategyVanilla import StrategyVanilla

st.set_page_config(page_title="Classic Options Pricer")

st.markdown("<h3 style='color:#336699;'>Classic Options Pricer</h3>", unsafe_allow_html=True)

col_left, _ = st.columns([1, 2])

with col_left:
    family = st.selectbox("Option family:", ["European", "Digital", "American"])

    option_type = None
    if family in ["European", "Digital", "American"]:
        cp_type = st.selectbox("Call or Put:", ["Call", "Put"])
        option_type = f"{family} {cp_type}"

    if option_type:
        pricer_choice = st.selectbox("Pricing model:", ["Black-Scholes", "Monte Carlo", "Trinomial Tree"])

        stock_price = st.number_input("Stock price:", min_value=0.0, value=100.0)
        dividend_yield = st.number_input("Dividend yield:", min_value=0.0, value=0.04)
        interest_rate = st.number_input("Interest rate:", min_value=0.0, value=0.02)
        volatility = st.number_input("Volatility:", min_value=0.0, value=0.2)
        strike = st.number_input("Strike:", min_value=0.0, value=100.0)

        pricing_date = st.date_input("Pricing date:", value=datetime(2024, 1, 1)).strftime("%Y-%m-%d")
        dividend_date = st.date_input("Dividend date:", value=datetime(2024, 6, 1)).strftime("%Y-%m-%d")
        maturity_date = st.date_input("Maturity date:", value=datetime(2025, 1, 1)).strftime("%Y-%m-%d")
        pricing_date_obj = datetime.strptime(pricing_date, "%Y-%m-%d")
        dividend_date_obj = datetime.strptime(dividend_date, "%Y-%m-%d")
        maturity_date_obj = datetime.strptime(maturity_date, "%Y-%m-%d")

        if family == "American":
            regression_type = st.selectbox("Regression type:", ["Classic", "Laguerre", "Hermite", "Legendre", "Tchebychev"])
            regression_degree = st.slider("Regression degree:", min_value=1, max_value=8, value=3)

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
            market = Market(stock_price, volatility, interest_rate, "Continuous", dividend_yield, 0, dividend_date_obj)

            if family == "European":
                option = OptionEuropean(cp_type, strike, maturity_date_obj)
            elif family == "Digital":
                option = OptionDigital(cp_type, strike, maturity_date_obj)
            elif family == "American":
                option = OptionAmerican(cp_type, strike, maturity_date_obj, regression_type, regression_degree)
            else:
                st.error("Type d'option non reconnu.")
                st.stop()

            if pricer_choice == "Black-Scholes":
                pricer = PricerBS(pricing_date_obj)
            elif pricer_choice == "Monte Carlo":
                pricer = PricerMC(pricing_date_obj, n_steps, n_draws, seed)
            elif pricer_choice == "Trinomial Tree":
                pricer = PricerTree(pricing_date_obj, n_steps, pruning_mode, pruning_limit)
            else:
                st.error("Modèle de pricing non reconnu.")
                st.stop()

            strategy = StrategyVanilla(market, option, pricer)
            price = strategy.price()

            st.session_state['pricing_result'] = f"Prix de la {option_type} avec {pricer_choice} : {round(price, 6)}"

if 'pricing_result' in st.session_state:
    st.success(st.session_state['pricing_result'])
