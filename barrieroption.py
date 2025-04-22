import streamlit as st
from datetime import datetime
from Market import Market
from OptionBarrier import OptionBarrier
from PricerMC import PricerMC
from StrategyVanilla import StrategyVanilla

st.set_page_config(page_title="Barrier Options Pricer")

st.markdown("<h3 style='color:#336699;'>Barrier Options Pricer</h3>", unsafe_allow_html=True)

col_left, _ = st.columns([1, 2])

with col_left:
    barrier_family = st.selectbox("Barrier Option type:", ["Knock-In Options", "Knock-Out Options"])

    barrier_type = None
    if barrier_family == "Knock-In Options":
        barrier_type = st.selectbox("Specific Option:", ["Down-and-In Call", "Down-and-In Put", "Up-and-In Call", "Up-and-In Put"])
    elif barrier_family == "Knock-Out Options":
        barrier_type = st.selectbox("Specific Option:", ["Down-and-Out Call", "Down-and-Out Put", "Up-and-Out Call", "Up-and-Out Put"])

    if barrier_type:
        cp_type = "Call" if "Call" in barrier_type else "Put"
        direction = "up" if "Up" in barrier_type else "down"
        knock_type = "in" if "In" in barrier_type else "out"

        stock_price = st.number_input("Stock price:", min_value=0.0, value=100.0)
        dividend_yield = st.number_input("Dividend yield:", min_value=0.0, value=0.035,step=0.001, format="%.5f")
        interest_rate = st.number_input("Interest rate:", min_value=0.0, value=0.02)
        volatility = st.number_input("Volatility:", min_value=0.0, value=0.2)
        strike = st.number_input("Strike:", min_value=0.0, value=100.0)
        barrier_level = st.number_input("Barrier level:", min_value=0.0, value=80.0)

        pricing_date = st.date_input("Pricing date:", value=datetime(2024, 1, 1))
        dividend_date = st.date_input("Dividend date:", value=datetime(2024, 6, 1))
        maturity_date = st.date_input("Maturity date:", value=datetime(2025, 1, 1))

        pricing_date_obj = datetime.combine(pricing_date, datetime.min.time())
        dividend_date_obj = datetime.combine(dividend_date, datetime.min.time())
        maturity_date_obj = datetime.combine(maturity_date, datetime.min.time())

        barrier_exercise = st.selectbox("Observation Style:", ["European", "American"])

        n_steps = st.number_input("Number of time steps:", min_value=1, value=100)
        n_draws = st.number_input("Number of paths:", min_value=1000, value=100000, step=1000)
        seed = st.number_input("Random seed:", min_value=0, value=1, step=1)

        if st.button("Price it!"):
            market = Market(stock_price, volatility, interest_rate, "Continuous", dividend_yield, 0, dividend_date_obj)
            pricer = PricerMC(pricing_date_obj, n_steps, n_draws, seed)
            option = OptionBarrier(cp_type, strike, maturity_date_obj, knock_type, direction, barrier_level, barrier_exercise)
            strategy = StrategyVanilla(market, option, pricer)

            price = strategy.price()
            st.success(f"Prix de l'option barrière '{barrier_type}' ({barrier_exercise}) : {round(price, 6)}")
