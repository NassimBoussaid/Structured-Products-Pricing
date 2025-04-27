import streamlit as st
from datetime import datetime
import numpy as np
import plotly.graph_objects as go

from structured_products_pricing.Parameters.Option.OptionAsian import OptionAsian
from structured_products_pricing.Parameters.Market import Market
from structured_products_pricing.Parameters.Pricer.PricerMC import PricerMC
from structured_products_pricing.Strategies.StrategiesOption.StrategyOptionVanilla import StrategyOptionVanilla

def run():
    # --- PAGE CONFIG
    st.markdown("<h3 style='color:#336699;'>Asian Options Pricer</h3>", unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 2])

    with col_left:
        st.subheader("Market Parameters")
        stock_price = st.number_input("Stock price:", min_value=0.0, value=100.0)
        interest_rt = st.number_input("Interest rate:", min_value=0.0, value=0.02)
        dividend_yld = st.number_input("Dividend yield:", min_value=0.0, value=0.035)
        volatility = st.number_input("Volatility:", min_value=0.0, value=0.2)

        st.subheader("Option Parameters")
        cp_type = st.selectbox("Option Type:", ["Call", "Put"])
        strike = st.number_input("Strike:", min_value=0.0, value=100.0)

        st.subheader("Dates")
        pricing_date = st.date_input("Pricing date:", value=datetime(2024, 1, 1))
        dividend_date = datetime(2024, 6, 1)
        maturity_date = st.date_input("Maturity date:", value=datetime(2025, 1, 1))

        st.subheader("Monte Carlo Parameters")
        n_steps = st.number_input("Number of time steps:", min_value=1, value=100)
        n_draws = st.number_input("Number of paths:", min_value=1000, value=20000, step=1000)
        seed = st.number_input("Random seed:", min_value=0, value=1, step=1)

        if cp_type != st.session_state.get("priced_cp_type", None):
            for key in ["strategy", "price", "greeks", "greeks_spot_range", "show_greeks", "show_graphs"]:
                if key in st.session_state:
                    del st.session_state[key]

        price_button = st.button("Price it!")

    with col_right:
        if price_button:
            with st.spinner("Pricing in progress..."):
                # Setup Market
                market = Market(
                    stock_price, volatility, interest_rt, "Continuous",
                    dividend_yld, 0.0, datetime.combine(maturity_date, datetime.min.time())
                )

                # Setup Option
                option = OptionAsian(cp_type, strike, datetime.combine(maturity_date, datetime.min.time()), "frequency")

                # Setup Pricer
                pricer = PricerMC(datetime.combine(pricing_date, datetime.min.time()), n_steps, n_draws, seed)

                # Setup Strategy
                strategy = StrategyOptionVanilla(market, option, pricer)

                # Run Pricing
                price = strategy.price()

                # Save in session
                st.session_state["strategy"] = strategy
                st.session_state["price"] = price
                st.session_state["priced_cp_type"] = cp_type
                st.session_state["greeks"] = None
                st.session_state["greeks_spot_range"] = None
                st.session_state["show_greeks"] = False
                st.session_state["show_graphs"] = False

        if "price" in st.session_state and "priced_cp_type" in st.session_state:
            if cp_type == st.session_state["priced_cp_type"]:
                st.success(f"Price of the {cp_type} Asian Option : **{round(st.session_state['price'], 4)}**")

                col_greek_button, col_graph_button = st.columns([1, 1])
                with col_greek_button:
                    if st.button("Get Greeks"):
                        st.session_state["show_greeks"] = True
                with col_graph_button:
                    if st.button("Get Graphs"):
                        st.session_state["show_graphs"] = True

        # Display Greeks
        if st.session_state.get("show_greeks", False):
            st.markdown(f"### Greeks : {cp_type} Asian Option")
            with st.spinner("Computing Greeks..." if st.session_state.get("greeks") is None else "Loading Greeks..."):
                if st.session_state.get("greeks") is None:
                    st.session_state["greeks"] = st.session_state["strategy"].greeks()
                greeks = st.session_state["greeks"]
                st.table({
                    "Greek": ["Delta", "Gamma", "Vega", "Theta", "Rho"],
                    "Value": [round(greeks[0], 4), round(greeks[1], 4),
                              round(greeks[2], 4), round(greeks[3], 4),
                              round(greeks[4], 4)]
                })

        # Display Graphs
        if st.session_state.get("show_graphs", False):
            st.markdown(f"### Graphs : {cp_type} Asian Option")
            with st.spinner("Loading Graphs..." if st.session_state.get("greeks_spot_range") is None else "Loading..."):
                if st.session_state.get("greeks_spot_range") is None:
                    st.session_state["greeks_spot_range"] = st.session_state["strategy"].greeks_over_spot_range(is_option=True)

                greeks_spot_range = st.session_state["greeks_spot_range"]

                tabs = st.tabs(["Payoff","Premium", "Delta", "Gamma", "Vega", "Theta", "Rho"])

                def plot_greek_simple(x, y, greek_name):
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=x, y=y,
                        mode='lines+markers',
                        name=greek_name
                    ))
                    fig.update_layout(
                        title=f"{greek_name} as a function of Spot",
                        xaxis_title="Spot",
                        yaxis_title=greek_name,
                        width=700,
                        height=450,
                        showlegend=False
                    )
                    st.plotly_chart(fig, use_container_width=True)

                with tabs[0]:
                    plot_greek_simple(greeks_spot_range['Spot'], greeks_spot_range['Payoff'], "Payoff")
                with tabs[1]:
                    plot_greek_simple(greeks_spot_range['Spot'], greeks_spot_range['Price'], "Premium")
                with tabs[2]:
                    plot_greek_simple(greeks_spot_range['Spot'], greeks_spot_range['Delta'], "Delta")
                with tabs[3]:
                    plot_greek_simple(greeks_spot_range['Spot'], greeks_spot_range['Gamma'], "Gamma")
                with tabs[4]:
                    plot_greek_simple(greeks_spot_range['Spot'], greeks_spot_range['Vega'], "Vega")
                with tabs[5]:
                    plot_greek_simple(greeks_spot_range['Spot'], greeks_spot_range['Theta'], "Theta")
                with tabs[6]:
                    plot_greek_simple(greeks_spot_range['Spot'], greeks_spot_range['Rho'], "Rho")
