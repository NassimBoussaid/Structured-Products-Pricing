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
        pricing_date = st.date_input("Pricing date:", value=datetime(2024, 1, 1))
        dividend_date = st.date_input("Dividend date:", value=datetime(2024, 6, 1))
        maturity_date = st.date_input("Maturity date:", value=datetime(2025, 1, 1))

        st.subheader("Monte Carlo Parameters")
        n_steps = st.number_input("Number of time steps:", min_value=1, value=100)
        n_draws = st.number_input("Number of paths:", min_value=1000, value=100_000, step=1000)
        seed = st.number_input("Random seed:", min_value=0, value=1, step=1)

        # --- Pricing Button
        price_button = st.button("Price it!")

    # --- Pricing Part
    with col_right:
        # Initialize session_state variables
        if "show_greeks" not in st.session_state:
            st.session_state["show_greeks"] = False
        if "show_graphs" not in st.session_state:
            st.session_state["show_graphs"] = False

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
                st.session_state["show_greeks"] = False
                st.session_state["show_graphs"] = False

        # Show Price if exists
        if "price" in st.session_state:
            st.success(f"Prix de l'option asiatique {cp_type} : **{round(st.session_state['price'], 6)}**")

            # Buttons for Greeks and Graphs
            col_greek_button, col_graph_button = st.columns([1, 1])
            with col_greek_button:
                if st.button("Get Greeks"):
                    st.session_state["show_greeks"] = True
            with col_graph_button:
                if st.button("Get Graphs"):
                    st.session_state["show_graphs"] = True
                    st.session_state["graph_loading"] = True

            # Display Titles if Greeks or Graphs selected
            if st.session_state["show_greeks"] or st.session_state["show_graphs"]:
                st.markdown(
                    f"""
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h3>Greeks : Asian Option</h3>
                        <h3>Graphs : Asian Option</h3>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                greeks_col1, greeks_col2 = st.columns([1, 2])

                # Left: Greeks
                with greeks_col1:
                    if st.session_state["show_greeks"]:
                        with st.spinner("Computing Greeks..."):
                            greeks = st.session_state["strategy"].greeks()

                            st.table({
                                "Greek": ["Delta", "Gamma", "Vega", "Theta", "Rho"],
                                "Value": [round(greeks[0], 4), round(greeks[1], 4),
                                          round(greeks[2], 4), round(greeks[3], 4),
                                          round(greeks[4], 4)]
                            })

                # Right: Graphs
                with greeks_col2:
                    if st.session_state.get("graph_loading", False):
                        with st.spinner("Loading Graphs..."):
                            greeks_spot_range = st.session_state["strategy"].greeks_over_spot_range()
                            st.session_state["greeks_spot_range"] = greeks_spot_range
                            st.session_state["graph_loading"] = False

                    if st.session_state["show_graphs"] and "greeks_spot_range" in st.session_state:
                        tabs = st.tabs(["Premium", "Delta", "Gamma", "Vega", "Theta", "Rho"])

                        def plot_greek_simple(x, y, greek_name):
                            fig = go.Figure()
                            fig.add_trace(go.Scatter(
                                x=x, y=y,
                                mode='lines+markers',
                                line=dict(color='orange'),
                                marker=dict(color='orange'),
                                name=greek_name
                            ))
                            fig.update_layout(
                                title=f"{greek_name} en fonction du Spot",
                                xaxis_title="Spot",
                                yaxis_title=greek_name,
                                width=700,
                                height=450,
                                showlegend=False,
                                plot_bgcolor="white",
                                paper_bgcolor="white",
                                margin=dict(l=20, r=20, t=40, b=20),
                                xaxis=dict(
                                    gridcolor='lightgrey',
                                    zeroline=False,
                                    showline=False,
                                ),
                                yaxis=dict(
                                    gridcolor='lightgrey',
                                    zeroline=False,
                                    showline=False,
                                ),
                            )
                            st.plotly_chart(fig, use_container_width=True)

                        greeks_spot_range = st.session_state["greeks_spot_range"]

                        with tabs[0]:
                            plot_greek_simple(greeks_spot_range['Spot'], greeks_spot_range['Price'], "Premium")
                        with tabs[1]:
                            plot_greek_simple(greeks_spot_range['Spot'], greeks_spot_range['Delta'], "Delta")
                        with tabs[2]:
                            plot_greek_simple(greeks_spot_range['Spot'], greeks_spot_range['Gamma'], "Gamma")
                        with tabs[3]:
                            plot_greek_simple(greeks_spot_range['Spot'], greeks_spot_range['Vega'], "Vega")
                        with tabs[4]:
                            plot_greek_simple(greeks_spot_range['Spot'], greeks_spot_range['Theta'], "Theta")
                        with tabs[5]:
                            plot_greek_simple(greeks_spot_range['Spot'], greeks_spot_range['Rho'], "Rho")
