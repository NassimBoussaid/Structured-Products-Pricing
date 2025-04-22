import streamlit as st
from datetime import datetime
from Market import Market
from PricerMC import PricerMC
from StrategyCertificateDiscount import StrategyCertificateDiscount
from StrategyCertificateAirbag import StrategyCertificateAirbag
from StrategyCertificateBonus import StrategyCertificateBonus
from StrategyCertificateCappedBonus import StrategyCertificateCappedBonus
from StrategyCertificateOutperformanceBonus import StrategyCertificateOutperformanceBonus
from StrategyCertificateTwinWin import StrategyCertificateTwinWin

st.set_page_config(page_title="Certificates Pricer")

st.markdown("<h3 style='color:#336699;'>Certificates Pricer</h3>", unsafe_allow_html=True)

col_left, _ = st.columns([1, 2])

with col_left:
    certificate_type = st.selectbox("Certificate Type :", [
        "Discount Certificate",
        "Bonus Certificate",
        "Capped Bonus Certificate",
        "Airbag Certificate",
        "Outperformance Bonus Certificate",
        "Twin-Win Certificate"
    ])

    stock_price = st.number_input("Stock price :", value=100.0)
    dividend_yield = st.number_input("Dividend yield :", value=0.035)
    interest_rate = st.number_input("Interest rate :", value=0.02)
    volatility = st.number_input("Volatility:", min_value=0.0, value=0.2)

    maturity_date = st.date_input("Maturity date:", value=datetime(2025, 1, 1))
    pricing_date = st.date_input("Pricing date:", value=datetime(2024, 1, 1))
    dividend_date = st.date_input("Dividend date:", value=datetime(2024, 6, 1))

    pricing_date_obj = datetime.combine(pricing_date, datetime.min.time())
    dividend_date_obj = datetime.combine(dividend_date, datetime.min.time())
    maturity_date_obj = datetime.combine(maturity_date, datetime.min.time())

    market = Market(stock_price,volatility, interest_rate, "Continuous", dividend_yield, 0, dividend_date_obj)
    pricer = PricerMC(pricing_date_obj, 100, 200000, 1)

    # Paramètres  selon le certificat
    if certificate_type == "Discount Certificate":
        cap = st.number_input("Cap :", value=115.0)
        if st.button("Price it!"):
            strat = StrategyCertificateDiscount(market, pricer, cap, maturity_date_obj)
            st.success(f"Discount Certificate Price : {round(strat.price(), 6)}")

    elif certificate_type == "Bonus Certificate":
        bonus = st.number_input("Bonus level:", value=110.0)
        barrier = st.number_input("Downside Put Barrier :", value=80.0)
        if st.button("Price it!"):
            strat = StrategyCertificateBonus(market, pricer, bonus, barrier, maturity_date_obj)
            st.success(f"Bonus Certificate Price : {round(strat.price(), 6)}")

    elif certificate_type == "Capped Bonus Certificate":
        bonus = st.number_input("Bonus level:", value=110.0)
        barrier = st.number_input("Downside Put Barrier :", value=80.0)
        cap = st.number_input("Cap :", value=120.0)
        if st.button("Price it!"):
            strat = StrategyCertificateCappedBonus(market, pricer, bonus, barrier, cap, maturity_date_obj)
            st.success(f"Capped Bonus Certificate Price : {round(strat.price(), 6)}")

    elif certificate_type == "Airbag Certificate":
        level = st.number_input("Participation level:", value=100.0)
        strike = st.number_input("Downside Put Strike :", value=85.0)
        if st.button("Price it!"):
            strat = StrategyCertificateAirbag(market, pricer, strike, level, maturity_date_obj)
            st.success(f"Airbag Certificate Price : {round(strat.price(), 6)}")

    elif certificate_type == "Outperformance Bonus Certificate":
        bonus = st.number_input("Bonus level:", value=110.0)
        barrier = st.number_input("Downside Put Barrier :", value=80.0)
        part = st.number_input("Upside Participation :", value=1.1)
        if st.button("Price it!"):
            strat = StrategyCertificateOutperformanceBonus(market, pricer, bonus, barrier, stock_price, maturity_date_obj)
            st.success(f"Outperformance Bonus Certificate Price : {round(strat.price(), 6)}")

    elif certificate_type == "Twin-Win Certificate":
        strike = st.number_input("Strike :", value=100.0)
        barrier = st.number_input("Downside Put Barrier :", value=80.0)
        if st.button("Price it!"):
            strat = StrategyCertificateTwinWin(market, pricer, strike, barrier, maturity_date_obj)
            st.success(f"Twin-Win Certificate Price : {round(strat.price(), 6)}")
