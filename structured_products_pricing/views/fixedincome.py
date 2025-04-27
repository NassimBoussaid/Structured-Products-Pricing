import streamlit as st
from datetime import datetime

def run():
    st.markdown("<h3 style='color:#336699;'>Fixed Income Pricer </h3>", unsafe_allow_html=True)

    col_left, col_right = st.columns([1, 2])

    with col_left:
        st.subheader("Market Parameters")
        issue_date = st.date_input("Issue Date:", value=datetime(2025, 1, 1))
        pricing_date = st.date_input("Pricing Date:", value=datetime(2025, 1, 1))
        maturity_date = st.date_input("Maturity Date:", value=datetime(2027, 1, 1))

        st.subheader("Product Selection")
        product_type = st.selectbox(
            "Product:",
            ["Zero Coupon Bond", "Fixed Rate Bond", "Floating Rate Bond", "Interest Rate Swap"]
        )

        # Product-specific parameters
        coupon_rate = None
        spread = None
        fixed_rate = None
        frequency = None
        day_count = None

        if product_type == "Fixed Rate Bond":
            coupon_rate = st.number_input("Coupon Rate:", min_value=0.0, value=0.05)
            frequency = st.selectbox("Coupon Frequency:", ["yearly", "semi-annual", "quarterly"])
            day_count = st.selectbox("Day Count Convention:", ["30/360", "act/360", "act/365.25"])

        if product_type == "Floating Rate Bond":
            spread = st.number_input("Spread (bps):", min_value=0.0, value=20.0) / 10000
            frequency = st.selectbox("Coupon Frequency:", ["monthly", "quarterly", "yearly"])
            day_count = st.selectbox("Day Count Convention:", ["30/360", "act/360", "act/365.25"])

        if product_type == "Interest Rate Swap":
            fixed_rate = st.number_input("Fixed Leg Rate:", min_value=0.0, value=0.02)
            spread = st.number_input("Floating Leg Spread (bps):", min_value=0.0, value=0.0) / 10000
            frequency = st.selectbox("Payment Frequency:", ["yearly", "semi-annual", "quarterly"])
            day_count = st.selectbox("Day Count Convention:", ["30/360", "act/360", "act/365.25"])



        show_button = st.button("Price it!")

