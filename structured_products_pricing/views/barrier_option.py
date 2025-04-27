import streamlit as st
from datetime import datetime
import plotly.graph_objects as go

from structured_products_pricing.Parameters.Option.OptionBarrier import OptionBarrier
from structured_products_pricing.Parameters.Market import Market
from structured_products_pricing.Parameters.Pricer.PricerMC import PricerMC
from structured_products_pricing.Strategies.StrategiesOption.StrategyOptionVanilla import StrategyOptionVanilla

def run():
    # --- PAGE CONFIG
    st.markdown("<h3 style='color:#336699;'>Barrier Options Pricer</h3>", unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 2])

    with col_left:
        st.subheader("Option Type")
        barrier_family = st.selectbox("Barrier Option type:", ["Knock-In Options", "Knock-Out Options"])
        barrier_type = st.selectbox(
            "Specific Option:",
            ["Down-and-In Call", "Down-and-In Put", "Up-and-In Call", "Up-and-In Put"]
            if barrier_family == "Knock-In Options"
            else ["Down-and-Out Call", "Down-and-Out Put", "Up-and-Out Call", "Up-and-Out Put"]
        )
        cp_type = "Call" if "Call" in barrier_type else "Put"
        direction = "up" if "Up" in barrier_type else "down"
        knock_type = "in" if "In" in barrier_type else "out"

        st.subheader("Market Parameters")
        stock_price = st.number_input("Stock price:", min_value=0.0, value=100.0)
        dividend_yld = st.number_input("Dividend yield:", min_value=0.0, value=0.035)
        volatility = st.number_input("Volatility:", min_value=0.0, value=0.2)

        rate_mode = st.selectbox("Rate Mode:", ["Constant", "Rate Curve", "Stochastic Rate"])
        if rate_mode == "Constant":
            interest_rt = st.number_input("Interest rate:", value=0.02)
        else:
            interest_rt = 0.02



        st.subheader("Option Parameters")
        strike = st.number_input("Strike:", min_value=0.0, value=100.0)

        # --- DEFAULT BARRIER LEVEL BASED ON BARRIER TYPE ---
        default_barrier_levels = {
            "Down-and-In Call": 90.0,
            "Down-and-In Put": 90.0,
            "Up-and-In Call": 110.0,
            "Up-and-In Put": 110.0,
            "Down-and-Out Call": 90.0,
            "Down-and-Out Put": 90.0,
            "Up-and-Out Call": 110.0,
            "Up-and-Out Put": 110.0
        }
        default_barrier_level = default_barrier_levels.get(barrier_type, 80.0)

        if "last_barrier_type" not in st.session_state:
            st.session_state["last_barrier_type"] = barrier_type

        if barrier_type != st.session_state["last_barrier_type"]:
            st.session_state["barrier_level_value"] = default_barrier_levels.get(barrier_type, 80.0)
            st.session_state["last_barrier_type"] = barrier_type

        barrier_level = st.number_input("Barrier level:", min_value=0.0,
                                        value=st.session_state.get("barrier_level_value", default_barrier_level),
                                        key="barrier_level_input")

        barrier_exercise = st.selectbox("Observation Style:", ["European", "American"])

        st.subheader("Dates")
        pricing_date = st.date_input("Pricing date:", value=datetime(2024, 1, 1))
        dividend_date = datetime(2024, 6, 1)
        maturity_date = st.date_input("Maturity date:", value=datetime(2025, 1, 1))

        st.subheader("Monte Carlo Parameters")
        n_steps = st.number_input("Number of time steps:", min_value=1, value=100)
        n_draws = st.number_input("Number of paths:", min_value=1000, value=20000, step=1000)
        seed = st.number_input("Random seed:", min_value=0, value=1, step=1)

        if barrier_type != st.session_state.get("priced_barrier_type", None):
            for key in ["strategy", "price", "greeks", "greeks_spot_range", "show_greeks", "show_graphs"]:
                if key in st.session_state:
                    del st.session_state[key]

        price_button = st.button("Price it!")

    with col_right:
        if price_button:
            with st.spinner("Pricing in progress..."):
                market = Market(
                    stock_price, volatility,rate_mode, interest_rt, "Continuous",
                    dividend_yld, 0.0, datetime.combine(dividend_date, datetime.min.time())
                )
                option = OptionBarrier(
                    cp_type, strike, datetime.combine(maturity_date, datetime.min.time()),
                    knock_type, direction, barrier_level, barrier_exercise
                )
                pricer = PricerMC(datetime.combine(pricing_date, datetime.min.time()), n_steps, n_draws, seed)
                strategy = StrategyOptionVanilla(market, option, pricer)

                price = strategy.price()

                st.session_state["strategy"] = strategy
                st.session_state["price"] = price
                st.session_state["priced_barrier_type"] = barrier_type
                st.session_state["greeks"] = None
                st.session_state["greeks_spot_range"] = None
                st.session_state["show_greeks"] = False
                st.session_state["show_graphs"] = False

        if "price" in st.session_state and "priced_barrier_type" in st.session_state:
            if barrier_type == st.session_state["priced_barrier_type"]:
                st.success(f"Price of the {barrier_type} {barrier_exercise} : **{round(st.session_state['price'], 4)}**")

                col_greek_button, col_graph_button = st.columns([1, 1])
                with col_greek_button:
                    if st.button("Get Greeks"):
                        st.session_state["show_greeks"] = True
                with col_graph_button:
                    if st.button("Get Graphs"):
                        st.session_state["show_graphs"] = True

        # Display Greeks
        if st.session_state.get("show_greeks", False):
            st.markdown(f"### Greeks : {barrier_type}")
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
            st.markdown(f"### Graphs : {barrier_type}")
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
