import streamlit as st



from datetime import datetime
import plotly.graph_objects as go

from structured_products_pricing.Parameters.Market import Market
from structured_products_pricing.Parameters.Pricer.PricerMC import PricerMC
from structured_products_pricing.Strategies.StrategiesCertificates.StrategyCertificateDiscount import StrategyCertificateDiscount
from structured_products_pricing.Strategies.StrategiesCertificates.StrategyCertificateAirbag import StrategyCertificateAirbag
from structured_products_pricing.Strategies.StrategiesCertificates.StrategyCertificateBonus import StrategyCertificateBonus
from structured_products_pricing.Strategies.StrategiesCertificates.StrategyCertificateCappedBonus import StrategyCertificateCappedBonus
from structured_products_pricing.Strategies.StrategiesCertificates.StrategyCertificateOutperformanceBonus import StrategyCertificateOutperformanceBonus
from structured_products_pricing.Strategies.StrategiesCertificates.StrategyCertificateTwinWin import StrategyCertificateTwinWin

def run():
    # --- PAGE CONFIG

    st.markdown("<h3 style='color:#336699;'>Certificates Pricer</h3>", unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 2])

    with col_left:
        st.subheader("Certificate Parameter")
        certificate_type = st.selectbox("Certificate Type :", [
            "Discount Certificate", "Bonus Certificate", "Capped Bonus Certificate",
            "Airbag Certificate", "Outperformance Bonus Certificate", "Twin-Win Certificate"
        ])
        # --- Specific Inputs per Certificate
        cap = bonus = barrier = strike = level = part = None

        if certificate_type == "Discount Certificate":
            cap = st.number_input("Cap :", value=115.0)

        elif certificate_type == "Bonus Certificate":
            bonus = st.number_input("Bonus level:", value=110.0)
            barrier = st.number_input("Downside Put Barrier :", value=80.0)

        elif certificate_type == "Capped Bonus Certificate":
            bonus = st.number_input("Bonus level:", value=110.0)
            barrier = st.number_input("Downside Put Barrier :", value=80.0)
            cap = st.number_input("Cap :", value=120.0)

        elif certificate_type == "Airbag Certificate":
            level = st.number_input("Participation level:", value=100.0)
            strike = st.number_input("Downside Put Strike :", value=85.0)

        elif certificate_type == "Outperformance Bonus Certificate":
            bonus = st.number_input("Bonus level:", value=110.0)
            barrier = st.number_input("Downside Put Barrier :", value=80.0)
            part = st.number_input("Upside Participation :", value=1.1)

        elif certificate_type == "Twin-Win Certificate":
            strike = st.number_input("Strike :", value=100.0)
            barrier = st.number_input("Downside Put Barrier :", value=80.0)

        st.subheader("Market Parameters")
        stock_price = st.number_input("Stock price :", value=100.0)
        dividend_yield = st.number_input("Dividend yield :", value=0.035)
        interest_rate = st.number_input("Interest rate :", value=0.02)
        volatility = st.number_input("Volatility:", min_value=0.0, value=0.2)

        st.subheader("Dates")
        maturity_date = st.date_input("Maturity date:", value=datetime(2025, 1, 1))
        pricing_date = st.date_input("Pricing date:", value=datetime(2024, 1, 1))
        dividend_date = st.date_input("Dividend date:", value=datetime(2024, 6, 1))

        st.subheader("Monte Carlo Parameters")
        n_steps = st.number_input("Number of time steps:", min_value=1, value=100)
        n_draws = st.number_input("Number of paths:", min_value=1000, value=100_000, step=1000)
        seed = st.number_input("Random seed:", min_value=0, value=1, step=1)

        # --- Price Button
        price_button = st.button("Price it!")

    # --- Pricing Part
    with col_right:
        if "show_greeks" not in st.session_state:
            st.session_state["show_greeks"] = False
        if "show_graphs" not in st.session_state:
            st.session_state["show_graphs"] = False

        pricing_date_obj = datetime.combine(pricing_date, datetime.min.time())
        dividend_date_obj = datetime.combine(dividend_date, datetime.min.time())
        maturity_date_obj = datetime.combine(maturity_date, datetime.min.time())

        market = Market(stock_price, volatility, interest_rate, "Continuous", dividend_yield, 0, dividend_date_obj)
        pricer = PricerMC(pricing_date_obj, n_steps, n_draws, seed)

        if price_button:
            with st.spinner("Pricing in progress..."):
                strategy = None

                if certificate_type == "Discount Certificate":
                    strategy = StrategyCertificateDiscount(market, pricer, cap, maturity_date_obj)

                elif certificate_type == "Bonus Certificate":
                    strategy = StrategyCertificateBonus(market, pricer, bonus, barrier, maturity_date_obj)

                elif certificate_type == "Capped Bonus Certificate":
                    strategy = StrategyCertificateCappedBonus(market, pricer, bonus, barrier, cap, maturity_date_obj)

                elif certificate_type == "Airbag Certificate":
                    strategy = StrategyCertificateAirbag(market, pricer, strike, level, maturity_date_obj)

                elif certificate_type == "Outperformance Bonus Certificate":
                    strategy = StrategyCertificateOutperformanceBonus(market, pricer, bonus, barrier, stock_price,
                                                                      maturity_date_obj)

                elif certificate_type == "Twin-Win Certificate":
                    strategy = StrategyCertificateTwinWin(market, pricer, strike, barrier, maturity_date_obj)

                if strategy is not None:
                    price = strategy.price()
                    st.session_state["strategy"] = strategy
                    st.session_state["price"] = price
                    st.session_state["show_greeks"] = False
                    st.session_state["show_graphs"] = False

        if "price" in st.session_state:
            st.success(f"{certificate_type} Price : **{round(st.session_state['price'], 6)}**")

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
                        <h3>Greeks : {certificate_type}</h3>
                        <h3>Graphs : {certificate_type}</h3>
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
