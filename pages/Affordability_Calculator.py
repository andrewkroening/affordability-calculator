"""This is the main app interface"""

import streamlit as st

from logic.mort_table_gen import (
    max_cost,
    build_rate_price_matrix,
)
from logic.mort_rate_scraper import get_rates
from logic.mort_afford_plot import cost_plot, heat_map

st.set_page_config(
    page_title="Affordability Calculator",
    page_icon="💲",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)


# Load data
today_rates = get_rates()
today_30 = today_rates["Rate_flt"][1].round(2)
today_30 = str(today_30)
today_30 = float(today_30)

# Create sidebar with the interest rates and an indicator for how the rate is changing
st.sidebar.title("Today's Rates")

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

# Create header
st.title("Affordability Calculator")
st.write(
    "Use this tool to help forecast what market changes will do to your home buying power. But definitely read the disclaimer at the bottom."
)

e1 = st.expander("Parameters", expanded=True)

with e1:
    st.caption("Use these sliders to configure your parameters.")
    max_pay = st.slider(
        "Max Monthly Payment",
        min_value=0,
        max_value=10_000,
        step=100,
        value=5_000,
    )
    max_down = st.slider(
        "Down Payment", min_value=0, max_value=500000, step=1_000, value=100_000
    )
    max_rate = st.slider(
        "Mortgage Interest Rate",
        min_value=0.0,
        max_value=10.0,
        step=0.01,
        value=today_30,
    )

max_list = max_cost(max_pay, max_down, max_rate, 30)

st.success(
    f"Based on your parameters, your maximum purchase price is \${max_list:,.2f}."
)

# Create the main content
st.markdown("---")

tab1, tab2 = st.tabs(["Affordability Summary", "Total Cost Comparison"])

with tab1:
    st.caption("This table shows the impact of price changes based on your parameters.")
    # price_table = price_afford_table(max_rate, max_down, 30, max_list)
    # st.table(price_table)
    table_test = build_rate_price_matrix(today_30, max_list, max_down)
    st.table(table_test)

    heat = heat_map()
    st.altair_chart(heat, use_container_width=True)

with tab2:
    st.caption(
        "These graphs show the difference in total costs between different terms."
    )
    cost_chart = cost_plot(max_list - max_down, today_rates)
    st.altair_chart(cost_chart, use_container_width=True)

st.markdown("---")

st.caption("Disclaimers")
st.caption("Mortgage insurance is not included in these estimates.")
