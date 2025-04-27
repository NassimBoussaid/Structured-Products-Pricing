import streamlit as st
import importlib

# GLOBAL CONFIG
st.set_page_config(
    page_title="Exotic Option Pricers",
    page_icon="💹",
    layout="wide",
)

# CLEAN SESSION STATE FUNCTION
def clear_pricing_session():
    pricing_keys = [
        "strategy", "price", "greeks", "greeks_spot_range",
        "show_greeks", "show_graphs",
        "priced_product_choice", "priced_strategy_type", "priced_cp_type",
        "priced_barrier_type", "priced_certificate_type", "priced_option_type",
        "priced_pricer_choice"
    ]
    for key in pricing_keys:
        if key in st.session_state:
            del st.session_state[key]

# PAGE DEFINITIONS
PAGES = {
    "Classic Options":    "views.classic_option",
    "Option Strategies":  "views.strategies_option",
    "Asian Options":      "views.asian_option",
    "Barrier Options":    "views.barrier_option",
    "Certificates":       "views.certificate",
    "Structured Products": "views.structured_products",
    "Fixed Income": "views.fixedincome",
}

# CURRENT STATE
if "active_page" not in st.session_state:
    st.session_state["active_page"] = "Home"
active_page = st.session_state["active_page"]

# NAVIGATION HELPER
def go_to(page_key: str) -> None:
    st.session_state["active_page"] = page_key
    st.rerun()

# SIDEBAR
with st.sidebar:
    st.title("Navigation")
    radio_key = f"nav_{active_page}"
    choice = st.radio(
        "Pages :",
        ["Home"] + list(PAGES.keys()),
        index=(0 if active_page == "Home"
               else 1 + list(PAGES.keys()).index(active_page)),
        key=radio_key,
    )

if choice != active_page:
    clear_pricing_session()
    st.session_state["active_page"] = choice
    active_page = choice
    st.rerun()

# HOME PAGE
if active_page == "Home":
    st.markdown(
        """
        <div style='text-align:center;'>
            <h2>Test our <span style='color:#0AB68B;'>Interactive Exotic Pricers</span></h2>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")

    cards = [
        {"title": "Classic Options",
         "subtitle": ["European options", "American options", "Digital options"],
         "key": "Classic Options"},
        {"title": "Option Strategies",
         "subtitle": ["Vertical Spreads", "Straddles & Strangles", "Butterfly & Condors"],
         "key": "Option Strategies"},
        {"title": "Asian Options",
         "subtitle": ["Asian Calls", "Asian Puts"],
         "key": "Asian Options"},
        {"title": "Barrier Options",
         "subtitle": ["Knock-In Options", "Knock-Out Options"],
         "key": "Barrier Options"},
        {"title": "Certificates",
         "subtitle": ["Bonus", "Airbag", "Twin-Win…"],
         "key": "Certificates"},
        {"title": "Structured Products",
         "subtitle": ["Reverse Convertibles", "Autocalls", "Barrier Reverse Convertibles"],
         "key": "Structured Products"},
        {"title": "Fixed Income",
         "subtitle": ["Zero Coupon Bond", "Fixed Rate Bond", "Floating Rate Bond", "Interest Rate Swap"],
         "key": "Fixed Income"},
    ]

    for row in range(0, len(cards), 3):
        cols = st.columns(3, gap="large")
        for col, card in zip(cols, cards[row:row + 3]):
            with col:
                st.markdown(
                    f"""
                    <div style="background:#ffffff10;border-radius:12px;
                                padding:30px 20px;text-align:center;
                                box-shadow:0 2px 6px rgba(0,0,0,0.15);">
                        <h4 style="margin-bottom:0.2rem;">{card['title']}</h4>
                        <p style="color:#8b9aa8;font-size:0.9rem;line-height:1.3rem;">
                            {'<br>'.join(card['subtitle'])}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.button(
                    "Try it now",
                    key=f"btn_{card['key']}",
                    use_container_width=True,
                    on_click=go_to,
                    args=(card["key"],),
                )

# FUNCTIONAL PAGES
else:
    if st.button("← Back to catalog"):
        go_to("Home")

    module = importlib.import_module(PAGES[active_page])
    module.run()
