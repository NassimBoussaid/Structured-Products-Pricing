import streamlit as st



from datetime import datetime
import plotly.graph_objects as go

from structured_products_pricing.Parameters.Market import Market
from structured_products_pricing.Parameters.Pricer.PricerMC import PricerMC
from structured_products_pricing.Parameters.Pricer.PricerTree import PricerTree
from structured_products_pricing.Parameters.Pricer.PricerBS import PricerBS

from structured_products_pricing.Parameters.Option.OptionEuropean import OptionEuropean
from structured_products_pricing.Parameters.Option.OptionDigital import OptionDigital
from structured_products_pricing.Parameters.Option.OptionAmerican import OptionAmerican

from structured_products_pricing.Strategies.StrategiesOption.StrategyOptionVanilla import StrategyOptionVanilla

def run():
    # --- PAGE CONFIG

    st.markdown("<h3 style='color:#336699;'>Classic Options Pricer</h3>", unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 2])

    with col_left:

        st.subheader("Pricing Model")
        pricer_choice = st.selectbox("Pricing model:", ["Black-Scholes", "Monte Carlo", "Trinomial Tree"])

        st.subheader("Market Parameters")

        if pricer_choice in ["Trinomial Tree", "Black-Scholes"]:
            family = "European"
            st.info(f"With {pricer_choice}, only European options are allowed.")
        else:
            family = st.selectbox("Option family:", ["European", "Digital", "American"])

        cp_type = st.selectbox("Call or Put:", ["Call", "Put"])
        option_type = f"{family} {cp_type}"

        stock_price = st.number_input("Stock price:", min_value=0.0, value=100.0)

        if pricer_choice == "Trinomial Tree":
            st.write("Dividend mode: Discrete (amount in €)")
            dividend_amount = st.number_input("Dividend amount (in €):", min_value=0.0, value=2.0)
            div_mode = "Discrete"
            dividend_yld = dividend_amount
        else:
            st.write("Dividend mode: Continuous (yield in %)")
            dividend_yld = st.number_input("Dividend yield (in %):", min_value=0.0, value=4.0, format="%.2f") / 100
            div_mode = "Continuous"

        interest_rate = st.number_input("Interest rate (in %):", min_value=0.0, value=2.0, format="%.2f") / 100
        volatility = st.number_input("Volatility (in %):", min_value=0.0, value=20.0, format="%.2f") / 100
        strike = st.number_input("Strike:", min_value=0.0, value=100.0)

        st.subheader("Dates")
        pricing_date = st.date_input("Pricing date:", value=datetime(2024, 1, 1))
        dividend_date = st.date_input("Dividend date:", value=datetime(2024, 6, 1))
        maturity_date = st.date_input("Maturity date:", value=datetime(2025, 1, 1))

        pricing_date_obj = datetime.combine(pricing_date, datetime.min.time())
        dividend_date_obj = datetime.combine(dividend_date, datetime.min.time())
        maturity_date_obj = datetime.combine(maturity_date, datetime.min.time())

        if family == "American":
            st.subheader("LSM Regression Parameters")
            regression_type = st.selectbox("Regression type:",
                                           ["Classic", "Laguerre", "Hermite", "Legendre", "Tchebychev"])
            regression_degree = st.slider("Regression degree:", min_value=1, max_value=8, value=3)

        st.subheader("Pricer Parameters")
        if pricer_choice == "Monte Carlo":
            n_steps = st.number_input("Number of time steps:", min_value=1, value=100)
            n_draws = st.number_input("Number of paths:", min_value=1000, value=100_000, step=1000)
            seed = st.number_input("Random seed:", min_value=0, value=1, step=1)
        elif pricer_choice == "Trinomial Tree":
            n_steps = st.number_input("Number of tree steps:", min_value=10, value=500, step=10)
            pruning_mode = st.radio("Apply pruning?", ["No", "Yes"], horizontal=True) == "Yes"
            pruning_limit = st.number_input("Pruning limit:", min_value=0.0, value=0.001, step=0.001, format="%f")

        # --- Price Button
        price_button = st.button("Price it!")

    with col_right:
        if "show_greeks" not in st.session_state:
            st.session_state["show_greeks"] = False
        if "show_graphs" not in st.session_state:
            st.session_state["show_graphs"] = False

        if price_button:
            with st.spinner("Pricing in progress..."):
                market = Market(stock_price, volatility, interest_rate, div_mode, dividend_yld, 0, dividend_date_obj)

                if family == "European":
                    option = OptionEuropean(cp_type, strike, maturity_date_obj)
                elif family == "Digital":
                    option = OptionDigital(cp_type, strike, maturity_date_obj)
                elif family == "American":
                    option = OptionAmerican(cp_type, strike, maturity_date_obj, regression_type, regression_degree)

                if pricer_choice == "Black-Scholes":
                    pricer = PricerBS(pricing_date_obj)
                elif pricer_choice == "Monte Carlo":
                    pricer = PricerMC(pricing_date_obj, n_steps, n_draws, seed)
                else:
                    pricer = PricerTree(pricing_date_obj, n_steps, pruning_mode, pruning_limit)

                strategy = StrategyOptionVanilla(market, option, pricer)
                price = strategy.price()

                st.session_state["strategy"] = strategy
                st.session_state["price"] = price
                st.session_state["show_greeks"] = False
                st.session_state["show_graphs"] = False

        if "price" in st.session_state:
            st.success(f"Prix de la {option_type} avec {pricer_choice} : **{round(st.session_state['price'], 6)}**")

            col_greek_button, col_graph_button = st.columns([1, 1])
            with col_greek_button:
                if st.button("Get Greeks"):
                    st.session_state["show_greeks"] = True
            with col_graph_button:
                if st.button("Get Graphs"):
                    st.session_state["show_graphs"] = True
                    st.session_state["graph_loading"] = True

            if st.session_state["show_greeks"] or st.session_state["show_graphs"]:
                st.markdown(
                    f"""
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h3>Greeks : {option_type}</h3>
                        <h3>Graphs : {option_type}</h3>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                greeks_col1, greeks_col2 = st.columns([1, 2])

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
