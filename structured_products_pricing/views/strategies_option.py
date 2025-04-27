import streamlit as st
from datetime import datetime
import plotly.graph_objects as go

from structured_products_pricing.Parameters.Market import Market
from structured_products_pricing.Parameters.Pricer.PricerMC import PricerMC

from structured_products_pricing.Strategies.StrategiesOption.StrategyCallSpread import StrategyCallSpread
from structured_products_pricing.Strategies.StrategiesOption.StrategyPutSpread import StrategyPutSpread
from structured_products_pricing.Strategies.StrategiesOption.StrategyStraddle import StrategyStraddle
from structured_products_pricing.Strategies.StrategiesOption.StrategyStrangle import StrategyStrangle
from structured_products_pricing.Strategies.StrategiesOption.StrategyButterflySpread import StrategyButterflySpread
from structured_products_pricing.Strategies.StrategiesOption.StrategyCondorSpread import StrategyCondorSpread
from structured_products_pricing.Strategies.StrategiesOption.StrategyDigitalReplication import StrategyDigitalReplication
from structured_products_pricing.Strategies.StrategiesOption.StrategyRiskReversal import StrategyRiskReversal
from structured_products_pricing.Strategies.StrategiesOption.StrategyStrap import StrategyStrap
from structured_products_pricing.Strategies.StrategiesOption.StrategyStrip import StrategyStrip

def run():
    st.markdown("<h3 style='color:#336699;'>Option Strategies Pricer</h3>", unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 2])

    with col_left:
        st.subheader("Strategy Parameters")
        strategy_type = st.selectbox("Option Strategy Type:", [
            "Call Spread", "Put Spread", "Straddle", "Strangle", "Butterfly Spread", "Condor Spread",
            "Digital Replication", "Risk Reversal", "Strap", "Strip", "Vanilla"
        ])
        strategy_map = {
            "Call Spread": 2,
            "Put Spread": 2,
            "Straddle": 1,
            "Strangle": 2,
            "Butterfly Spread": 3,
            "Condor Spread": 4,
            "Digital Replication": 1,
            "Risk Reversal": 2,
            "Strap": 1,
            "Strip": 1,
            "Vanilla": 1
        }
        n_options = strategy_map.get(strategy_type, 2)

        option_strikes = []
        for i in range(n_options):
            strike = st.number_input(f"Strike {i + 1}", value=100.0 + 5 * i, key=f"strike_{i}")
            option_strikes.append(strike)

        epsilon = None
        option_type = None
        if strategy_type == "Digital Replication":
            epsilon = st.number_input("Epsilon (spread width):", value=1.0)
            option_type = st.selectbox("Option type:", ["Call", "Put"])

        st.subheader("Market Parameters")
        stock_price = st.number_input("Stock price:", min_value=0.0, value=100.0)
        dividend_yield = st.number_input("Dividend yield:", min_value=0.0, value=0.035)
        volatility = st.number_input("Volatility:", min_value=0.0, value=0.2)

        rate_mode = st.selectbox("Rate Mode:", ["Constant", "Rate Curve", "Stochastic Rate"])
        if rate_mode == "Constant":
            interest_rate = st.number_input("Interest rate:", value=0.02)
        else:
            interest_rate = 0.02


        st.subheader("Dates")
        pricing_date = st.date_input("Pricing date:", value=datetime(2024, 1, 1))
        dividend_date = datetime(2024, 6, 1)
        maturity_date = st.date_input("Maturity date:", value=datetime(2025, 1, 1))

        pricing_date_obj = datetime.combine(pricing_date, datetime.min.time())
        dividend_date_obj = datetime.combine(dividend_date, datetime.min.time())
        maturity_date_obj = datetime.combine(maturity_date, datetime.min.time())

        st.subheader("Monte Carlo Parameters")
        n_steps = st.number_input("Number of time steps:", min_value=1, value=100)
        n_draws = st.number_input("Number of paths:", min_value=1000, value=20000, step=1000)
        seed = st.number_input("Random seed:", min_value=0, value=1, step=1)

        if strategy_type != st.session_state.get("priced_strategy_type", None):
            for key in ["strategy", "price", "greeks", "greeks_spot_range", "show_greeks", "show_graphs"]:
                if key in st.session_state:
                    del st.session_state[key]

        price_button = st.button("Price this strategy!")

    with col_right:
        if price_button:
            with st.spinner("Pricing in progress..."):
                market = Market(stock_price, volatility,rate_mode, interest_rate, "Continuous", dividend_yield, 0, dividend_date_obj)
                pricer = PricerMC(pricing_date_obj, n_steps, n_draws, seed)

                strat = None
                if strategy_type == "Call Spread":
                    strat = StrategyCallSpread(market, pricer, option_strikes[0], option_strikes[1], maturity_date_obj)
                elif strategy_type == "Put Spread":
                    strat = StrategyPutSpread(market, pricer, option_strikes[0], option_strikes[1], maturity_date_obj)
                elif strategy_type == "Straddle":
                    strat = StrategyStraddle(market, pricer, option_strikes[0], maturity_date_obj)
                elif strategy_type == "Strangle":
                    strat = StrategyStrangle(market, pricer, option_strikes[0], option_strikes[1], maturity_date_obj)
                elif strategy_type == "Butterfly Spread":
                    strat = StrategyButterflySpread(market, pricer, option_strikes[0], option_strikes[1],
                                                    option_strikes[2], maturity_date_obj)
                elif strategy_type == "Condor Spread":
                    strat = StrategyCondorSpread(market, pricer, option_strikes[0], option_strikes[1],
                                                 option_strikes[2], option_strikes[3], maturity_date_obj)
                elif strategy_type == "Digital Replication":
                    strat = StrategyDigitalReplication(market, pricer, option_type, option_strikes[0], epsilon,
                                                       maturity_date_obj)
                elif strategy_type == "Risk Reversal":
                    strat = StrategyRiskReversal(market, pricer, option_strikes[0], option_strikes[1],
                                                 maturity_date_obj)
                elif strategy_type == "Strap":
                    strat = StrategyStrap(market, pricer, option_strikes[0], maturity_date_obj)
                elif strategy_type == "Strip":
                    strat = StrategyStrip(market, pricer, option_strikes[0], maturity_date_obj)
                else:
                    st.error("Stratégie non reconnue.")
                    st.stop()

                price = strat.price()

                st.session_state["strategy"] = strat
                st.session_state["price"] = price
                st.session_state["priced_strategy_type"] = strategy_type
                st.session_state["greeks"] = None
                st.session_state["greeks_spot_range"] = None
                st.session_state["show_greeks"] = False
                st.session_state["show_graphs"] = False

        if "price" in st.session_state and "priced_strategy_type" in st.session_state:
            if strategy_type == st.session_state["priced_strategy_type"]:
                st.success(f"Price of the {strategy_type} Strategy : **{round(st.session_state['price'], 2)}**")

                col_greek_button, col_graph_button = st.columns([1, 1])
                with col_greek_button:
                    if st.button("Get Greeks"):
                        st.session_state["show_greeks"] = True
                with col_graph_button:
                    if st.button("Get Graphs"):
                        st.session_state["show_graphs"] = True

        # Greeks Section
        if st.session_state.get("show_greeks", False):
            st.markdown(f"### Greeks : {strategy_type}")
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

        # Graphs Section
        if st.session_state.get("show_graphs", False):
            st.markdown(f"### Graphs : {strategy_type}")
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
