import streamlit as st
from datetime import datetime
import numpy as np
import plotly.graph_objects as go

from structured_products_pricing.Parameters.Market import Market
from structured_products_pricing.Parameters.Pricer.PricerMC import PricerMC
from structured_products_pricing.Strategies.StrategiesStructured.StrategyStructuredBarrierReverseConvertible import StrategyStructuredBarrierReverseConvertible
from structured_products_pricing.Strategies.StrategiesStructured.StrategyStructuredAutocall import StrategyStructuredAutocall
from structured_products_pricing.Strategies.StrategiesStructured.StrategyStructuredReverseConvertible import StrategyStructuredReverseConvertible

def run():
    st.markdown("<h3 style='color:#336699;'>Structured Products Pricer</h3>", unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 2])

    with col_left:
        st.subheader("Product")
        product_choice = st.selectbox("Choose the product to price:",
                                      ["Barrier Reverse Convertible", "Autocall", "Reverse Convertible"])

        st.subheader("Market Parameters")
        stock_price = st.number_input("Stock price:", min_value=0.0, value=100.0)
        dividend_yld = st.number_input("Dividend yield:", min_value=0.0, value=0.035)
        volatility = st.number_input("Volatility:", min_value=0.0, value=0.2)

        rate_mode = st.selectbox("Rate Mode:", ["Constant", "Rate Curve", "Stochastic Rate"])
        if rate_mode == "Constant":
            interest_rt = st.number_input("Interest rate:", value=0.02)
        else:
            interest_rt = 0.02


        st.subheader("Product Parameters")
        if product_choice == "Barrier Reverse Convertible":
            strike = st.number_input("Strike (% of Spot):", min_value=0.0, value=100.0)
            barrier_level = st.number_input("Barrier Level (% of Spot):", min_value=0.0, value=80.0)
            coupon_level = st.number_input("Coupon Level (absolute amount):", min_value=0.0, value=0.1)
        elif product_choice == "Autocall":
            strike_pdi = st.number_input("Strike PDI (% of Spot):", min_value=0.0, value=100.0)
            barrier_pdi = st.number_input("Barrier PDI (% of Spot):", min_value=0.0, value=80.0)
            barrier_autocall = st.number_input("Autocall Barrier (% of Spot):", min_value=0.0, value=100.0)
            barrier_coupon = st.number_input("Coupon Barrier (% of Spot):", min_value=0.0, value=100.0)
            coupon_level = st.number_input("Coupon Level (per period):", min_value=0.0, value=0.01)
            coupon_frequency = st.selectbox("Coupon Frequency:", ["monthly", "annually"])
        elif product_choice == "Reverse Convertible":
            strike = st.number_input("Strike (% of Spot):", min_value=0.0, value=100.0)
            coupon_level = st.number_input("Coupon Level (annualized %):", min_value=0.0, value=0.1)

        st.subheader("Dates")
        pricing_date = st.date_input("Pricing date:", value=datetime(2024, 1, 1))
        maturity_date = st.date_input("Maturity date:", value=datetime(2025, 1, 1))

        pricing_datetime = datetime.combine(pricing_date, datetime.min.time())
        maturity_datetime = datetime.combine(maturity_date, datetime.min.time())
        dividend_datetime = datetime(2024, 6, 1)

        st.subheader("Monte Carlo Parameters")
        n_steps = st.number_input("Number of time steps:", min_value=1, value=50)
        n_draws = st.number_input("Number of paths:", min_value=1000, value=20000, step=1000)
        seed = st.number_input("Random seed:", min_value=0, value=1, step=1)

        if product_choice != st.session_state.get("priced_product_choice", None):
            for key in ["strategy", "price", "greeks", "greeks_spot_range", "show_greeks", "show_graphs"]:
                if key in st.session_state:
                    del st.session_state[key]



        price_button = st.button("Price it!")

    with col_right:
        if price_button:
            with st.spinner("Pricing in progress..."):
                market = Market(
                    underlying_price=stock_price,
                    volatility=volatility,
                    rate_mode=rate_mode,
                    interest_rate=interest_rt,
                    div_mode="Continuous",
                    dividend_rate=dividend_yld,
                    dividend_discrete=0.00,
                    dividend_date=dividend_datetime
                )

                pricer_mc = PricerMC(
                    pricing_date=pricing_datetime,
                    nb_steps=n_steps,
                    nb_draws=n_draws,
                    seed=seed
                )

                if product_choice == "Barrier Reverse Convertible":
                    strategy = StrategyStructuredBarrierReverseConvertible(
                        MarketObject=market,
                        PricerObject=pricer_mc,
                        strike=strike,
                        barrier_level=barrier_level,
                        coupon_level=coupon_level,
                        maturity_date=maturity_datetime
                    )
                elif product_choice == "Autocall":
                    strategy = StrategyStructuredAutocall(
                        MarketObject=market,
                        PricerObject=pricer_mc,
                        strike_pdi=strike_pdi,
                        barrier_pdi=barrier_pdi,
                        barrier_autocall=barrier_autocall,
                        barrier_coupon=barrier_coupon,
                        coupon_level=coupon_level,
                        coupon_frequency=coupon_frequency,
                        maturity_date=maturity_datetime
                    )
                elif product_choice == "Reverse Convertible":
                    strategy = StrategyStructuredReverseConvertible(
                        MarketObject=market,
                        PricerObject=pricer_mc,
                        strike=strike,
                        coupon_level=coupon_level,
                        maturity_date=maturity_datetime
                    )

                price = strategy.price()

                # Save to session state
                st.session_state["strategy"] = strategy
                st.session_state["price"] = price
                st.session_state["priced_product_choice"] = product_choice

                # Reset Greeks and Graphs
                st.session_state["greeks"] = None
                st.session_state["greeks_spot_range"] = None
                st.session_state["show_greeks"] = False
                st.session_state["show_graphs"] = False

        if "price" in st.session_state and "priced_product_choice" in st.session_state:
            if product_choice == st.session_state["priced_product_choice"]:
                st.success(f"Price of the {product_choice} : **{round(st.session_state['price'], 2)}%**")

                col_greek_button, col_graph_button = st.columns([1, 1])
                with col_greek_button:
                    if st.button("Get Greeks"):
                        st.session_state["show_greeks"] = True
                with col_graph_button:
                    if st.button("Get Graphs"):
                        st.session_state["show_graphs"] = True

        # Display Greeks
        if st.session_state.get("show_greeks", False):
            st.markdown(f"### Greeks : {product_choice}")
            with st.spinner("Computing Greeks..." if st.session_state["greeks"] is None else "Loading Greeks..."):
                if st.session_state["greeks"] is None:
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
            st.markdown(f"### Graphs : {product_choice}")
            with st.spinner("Loading Graphs..." if st.session_state["greeks_spot_range"] is None else "Loading..."):
                if st.session_state["greeks_spot_range"] is None:
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
