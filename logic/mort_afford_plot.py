"""This is the plot function to show the affordability table"""


import altair as alt
import pandas as pd
import numpy as np

from logic.mort_table_gen import mortgage_cost


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


def heat_map():
    """This shows a heat map of the total cost of the mortgage for different options"""

    # make a copy of the rate_df
    # cost_matrix = cost_matrix.copy()

    # # Create the chart
    # chart = (
    #     alt.Chart(cost_matrix)
    #     .mark_rect()
    #     .encode(
    #         x=alt.X("Rates:Q", title="Interest Rate", scale=alt.Scale(zero=False)),
    #         y=alt.Y(
    #             "Price:Q",
    #             title="Sale Price",
    #             scale=alt.Scale(zero=False),
    #         ),
    #         color=alt.Color(
    #             "Payment:Q",
    #             title="Payment",
    #             scale=alt.Scale(zero=False),
    #         ),
    #     )
    # )

    # Compute x^2 + y^2 across a 2D grid
    x, y = np.meshgrid(range(-5, 5), range(-5, 5))
    z = x**2 + y**2

    # Convert this grid to columnar data expected by Altair
    source = pd.DataFrame({"x": x.ravel(), "y": y.ravel(), "z": z.ravel()})

    chart = alt.Chart(source).mark_rect().encode(x="x:O", y="y:O", color="z:Q")

    return chart
