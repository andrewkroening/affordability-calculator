"""This is the main app module"""

import streamlit as st

from logic.mort_logic import (
    get_rates,
    max_cost,
    # mortgage_cost,
    rate_price_matrix,
    # cost_plot,
    heat_map,
)


st.set_page_config(
    page_title="Fun Money Tools",
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
    # if row["Change"] != "Unchanged":
    #     st.sidebar.metric(
    #         label=row["Program"],
    #         value=f"{row['Rate']}",
    #         delta=f"{row['Change']}",
    #         delta_color="inverse",
    #     )
    # else:
    st.sidebar.metric(
        label=row["Product"],
        value=f"{row['Rate']}",
        delta_color="inverse",
    )
    # st.sidebar.caption("Unchanged")

st.sidebar.markdown("---")
st.sidebar.markdown(
    "Source: [Bankrate](https://www.bankrate.com/mortgages/mortgage-rates/#mortgage-industry-insights)"
)

st.title("Welcome to Fun Money Tools")
st.write(
    "Learning about finance is hard, and sometimes it can be really intimidating. This is a collection of tools to help you manage your money and learn some practices along the way. It's set up to help you answer some common questions that you might have while you navigate some potentially sticky situations."
)
st.write(" ")
st.write(
    "Figuring out how to manage your money can be really hard. Check out the tools below to get started."
)

tab1, tab2 = st.tabs(["Budgeting Tool", "Home Buying Calculator"])

with tab1:
    st.caption(
        "Figuring out what you can (and can't do) can be frustrating and confusing. This tool will help you figure out how much you can afford to spend on a few major, common categories."
    )

with tab2:
    # Create header
    st.write(
        "Buying a home is a big decision, and it's important to know what you can afford. This tool will help you figure out how much you can afford to spend on a home, and how much you can expect to pay each month based on a few parameters."
    )

    st.write(
        "Use this tool to help forecast what market changes will do to your home buying power."
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
        f"Based on the parameters, your maximum purchase price is \${max_list:,.2f}."
    )

    # Create the main content

    tab3, tab4 = st.tabs(["Affordability Summary", "Total Cost Comparison"])

    with tab3:
        st.caption(
            "This table shows the impact of price changes based on your parameters."
        )
        r_p_table = rate_price_matrix(max_rate, max_list, max_down)

        heat = heat_map(r_p_table)
        st.altair_chart(heat, use_container_width=True, theme="streamlit")

    with tab4:
        st.caption(
            "These graphs show the difference in total costs between different terms."
        )
        # cost_chart = cost_plot(max_list - max_down, today_rates)
        # st.altair_chart(cost_chart, use_container_width=True)
