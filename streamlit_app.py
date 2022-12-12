"""This is the main app interface"""

import streamlit as st

from logic.table_gen import price_afford_table, rate_afford_table
from logic.rate_scraper import get_rates

st.set_page_config(
    page_title="Affordability Calculator",
    page_icon="💲",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)


# Load data
today_rates = get_rates()

# Create header
st.title("Affordability Calculator")
st.write(
    "Use this tool to help forecast what market changes will do to your home buying power. But definitely read the disclaimer at the bottom."
)

# Create sidebar with the interest rates and an indicator for how the rate is changing
st.sidebar.title("Today's Rates")
st.sidebar.markdown("---")

for index, row in today_rates.iterrows():
    if row["Change"] != "Unchanged":
        st.sidebar.metric(
            label=row["Program"],
            value=f"{row['Rate']}",
            delta=f"{row['Change']}",
            delta_color="inverse",
        )
    else:
        st.sidebar.metric(
            label=row["Program"],
            value=f"{row['Rate']}",
            delta_color="inverse",
        )
        st.sidebar.caption("Unchanged")

    st.sidebar.markdown("---")
    st.sidebar.markdown(
        "Source: [The Mortgage Reports](https://themortgagereports.com/today)"
    )

# Create the main content
st.markdown("---")
today_30 = today_rates["Rate_flt"][1].round(2)
today_30 = str(today_30)
today_30 = float(today_30)

st.write("This is where the final conclusion piece will go.")

st.slider("Max Monthly Payment", min_value=0, max_value=10000, step=100, value=5000)
st.slider("Down Payment", min_value=0, max_value=500000, step=1000, value=100000)
st.slider(
    "Mortgage Interest Rate",
    min_value=0.0,
    max_value=10.0,
    step=0.01,
    value=today_30,
)

tab1, tab2, tab3 = st.tabs(
    ["Price Affordability", "Rate Affordability", "Total Cost Comparison"]
)

st.table(today_rates)
