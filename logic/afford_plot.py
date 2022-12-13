"""This is the plot function to show the affordability table"""


import altair as alt

from logic.table_gen import mortgage_cost


def cost_plot(max_list, rate_df):
    """This shows a bar chart of the total cost of the mortgage for different year options"""

    # make a copy of the rate_df
    rate_df = rate_df.copy()

    # add the total cost of the mortgage to the rate_df
    rate_df["Total Cost"] = rate_df["Rate_flt"].apply(
        lambda x: mortgage_cost(max_list, x, 30)[1]
    )

    # keep the top four rows and sort by Total Cost
    rate_df = rate_df.sort_values(by="Total Cost").head(11)

    # Create the chart
    chart = (
        alt.Chart(rate_df)
        .mark_bar()
        .encode(
            x=alt.X("Years:Q", title="Length of Mortgage", scale=alt.Scale(zero=False)),
            y=alt.Y(
                "Total Cost:Q",
                title="Total Cost of Mortgage",
                scale=alt.Scale(zero=False),
            ),
        )
    )

    return chart
