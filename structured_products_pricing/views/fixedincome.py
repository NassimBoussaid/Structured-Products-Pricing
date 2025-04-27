import streamlit as st
from datetime import datetime, date, time
from structured_products_pricing.Parameters.Bond.BondFixedRate import FixedRateBond
from structured_products_pricing.Parameters.Bond.BondFloatingRate import FloatingRateBond
from structured_products_pricing.Parameters.Bond.InterestRateSwap import InterestRateSwap
from structured_products_pricing.Parameters.Bond.BondZC import ZeroCouponBond
from structured_products_pricing.Products.Bond.RatePricerManager import RatePricerManager
from structured_products_pricing.Parameters.Market import Market


def run():
    st.markdown("<h3 style='color:#336699;'>Fixed Income Pricer</h3>", unsafe_allow_html=True)
    col_left, col_right = st.columns([1, 2])


    with col_left:
        st.subheader("Market Parameters")
        issue_date_d  = st.date_input("Issue Date:",    value=date(2025, 1, 1))
        pricing_date_d = st.date_input("Pricing Date:", value=date(2025, 1, 1))
        maturity_date_d = st.date_input("Maturity Date:", value=date(2027, 1, 1))

        st.subheader("Product Selection")
        product_type = st.selectbox(
            "Product:",
            ["Zero Coupon Bond", "Fixed Rate Bond", "Floating Rate Bond", "Interest Rate Swap"]
        )

        # Product-specific parameters
        coupon_rate = spread = fixed_rate = None
        frequency = day_count = None

        if product_type == "Fixed Rate Bond":
            coupon_rate = st.number_input("Coupon Rate:", min_value=0.0, value=0.05)
            frequency   = st.selectbox("Coupon Frequency:", ["yearly", "semi-annual", "quarterly"])
            day_count   = st.selectbox("Day Count Convention:", ["30/360", "act/360", "act/365.25"])

        elif product_type == "Floating Rate Bond":
            spread      = st.number_input("Spread (bps):", min_value=0.0, value=20.0) / 1e4
            frequency   = st.selectbox("Coupon Frequency:", ["monthly", "quarterly", "yearly"])
            day_count   = st.selectbox("Day Count Convention:", ["30/360", "act/360", "act/365.25"])

        elif product_type == "Interest Rate Swap":
            fixed_rate  = st.number_input("Fixed Leg Rate:", min_value=0.0, value=0.02)
            spread      = st.number_input("Floating Leg Spread (bps):", min_value=0.0, value=0.0) / 1e4
            frequency   = st.selectbox("Payment Frequency:", ["yearly", "semi-annual", "quarterly"])
            day_count   = st.selectbox("Day Count Convention:", ["30/360", "act/360", "act/365.25"])

        show_button = st.button("Price it!")


    if show_button:

        issue_date_str    = issue_date_d.strftime("%Y-%m-%d")
        maturity_date_str = maturity_date_d.strftime("%Y-%m-%d")
        pricing_date_dt   = datetime.combine(pricing_date_d, time.min)


        Market_Info = Market(
            100, 0.2, "constant", 0.02, "Continuous",
            0.035, 0, datetime(2024, 6, 1)
        )


        if product_type == "Zero Coupon Bond":
            product = ZeroCouponBond(
                notional=1,
                issue_date=issue_date_str,
                maturity_date=maturity_date_str
            )
        elif product_type == "Fixed Rate Bond":
            product = FixedRateBond(
                notional=1,
                issue_date=issue_date_str,
                maturity_date=maturity_date_str,
                coupon_rate=coupon_rate,
                frequency=frequency,
                day_count=day_count
            )
        elif product_type == "Floating Rate Bond":
            product = FloatingRateBond(
                notional=1,
                issue_date=issue_date_str,
                maturity_date=maturity_date_str,
                spread=spread,
                frequency=frequency,
                day_count=day_count
            )
        elif product_type == "Interest Rate Swap":
            product = InterestRateSwap(
                notional=1,
                issue_date=issue_date_str,
                maturity_date=maturity_date_str,
                fixed_rate=fixed_rate,
                spread=spread,
                frequency=frequency,
                day_count=day_count
            )


        pricer = RatePricerManager(
            MarketObject=Market_Info,
            BondObject=product,
            pricing_date=pricing_date_dt
        )
        price = pricer.compute_price()


        st.success(f"Price of the {product_type} : {price:.4f}")



