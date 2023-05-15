"""This is the logic file for the mortgage calculator functions"""

import altair as alt
import pandas as pd
import numpy as np
import numpy_financial as npf


def get_rates():
    """Gets the daily mortgage rates from The Mortgage Reports

    Returns:
        rate_data (DataFrame): A DataFrame of the daily mortgage rates"""

    # getthe rates from the mortgage reports
    rate_data = pd.read_html("https://themortgagereports.com/mortgage-rates-now")
    rate_data = rate_data[0]

    # rename the columns to Program, Rate, APR, Change
    rate_data.columns = ["Program", "Rate", "APR", "Change"]

    # drop nas
    rate_data.dropna(inplace=True)

    # filter rate data to include only columns with a % in the rate column
    rate_data = rate_data[rate_data["Rate"].str.contains("%")]

    # make a column with the rate as a float
    rate_data["Rate_flt"] = rate_data["Rate"].astype(str)

    # drop the % from the rate column
    rate_data["Rate_flt"] = rate_data["Rate_flt"].str.replace("%", "")

    # convert the rate column to a float
    rate_data["Rate_flt"] = rate_data["Rate_flt"].astype(float)

    # make a column with the APR as a float
    rate_data["APR_flt"] = rate_data["APR"].astype(str)

    # drop the % from the rate column
    rate_data["APR_flt"] = rate_data["APR_flt"].str.replace("%", "")

    # convert the rate column to a float
    rate_data["APR_flt"] = rate_data["APR_flt"].astype(float)

    # make a years column
    rate_data["Years"] = rate_data["Program"].str.extract(r"(\d+)")

    return rate_data


def max_cost(max_pay, max_down, max_rate, term):
    """This function calculates the maximum purchase price.

    Args:
        max_pay (int): The maximum monthly payment.
        max_down (int): The maximum down payment.
        max_rate (float): The maximum interest rate.
        term (int): The term of the mortgage in years.

    Returns:
        max_total (int): The maximum purchase price.
    """

    # Calculate the maximum purchase price using pv
    max_price = npf.pv(max_rate / 100 / 12, term * 12, max_pay, when="begin")

    # Calculate the maximum principal
    max_total = max_price - max_down

    return abs(max_total)


def mortgage_cost(principal, rate, term):
    """This function calculates the cost of a mortgage.

    Args:
        principal (int): The principal of the mortgage.
        rate (float): The interest rate of the mortgage.
        term (int): The term of the mortgage in years.

    Returns:
        payment (float): The monthly payment.
    """

    # Calculate the monthly payment
    monthly_rate = rate / 100 / 12
    payments = term * 12
    payment = (
        principal
        * (monthly_rate * (1 + monthly_rate) ** payments)
        / ((1 + monthly_rate) ** payments - 1)
    )

    # Calculate the total cost of the mortgage
    total_cost = payment * payments

    # Calculate the total interest paid
    interest_paid = total_cost - principal

    return payment, total_cost, interest_paid


def rate_price_matrix(int_rate, pay_price, down_payment):
    """This function builds a matrix of affordability.

    Args:
        int_rate (float): The interest rate of the mortgage.
        pay_price (int): The purchase price of the home.
        down_payment (int): The down payment of the mortgage.

    Returns:
        rate_price_matrix (DataFrame): A DataFrame of the affordability matrix."""

    # generate a list of sale prices with the pay_price as the center
    price_minus = pay_price - (pay_price * 0.25)
    price_plus = pay_price + (pay_price * 0.25)
    price_list = [
        x for x in range(int(price_minus), int(price_plus), int(pay_price * 0.05))
    ]

    # round price_list to the nearst 1000
    price_list = [round(x, -3) for x in price_list]

    # generate a list of interest rates with the int_rate as the center
    rate_list = [x for x in range(200, 1100, 50)]
    rate_list = [x / 100 for x in rate_list]

    # add the int_rate to the list and sort the list
    rate_list.append(int_rate)
    rate_list = sorted(rate_list)

    # filter the table for int_rate +/- 2
    rate_list = [x for x in rate_list if x >= int_rate - 2 and x <= int_rate + 2]

    # create a dataframe from the rate_list and price_list
    rate_price_matrix = pd.DataFrame(columns=rate_list, index=price_list)

    # # populate the dataframe with the payment values
    for rate in rate_list:
        for price in price_list:
            rate_price_matrix.loc[price, rate] = mortgage_cost(
                price - down_payment, rate, 30
            )[0]

    # # convert all values to integers
    rate_price_matrix = rate_price_matrix.astype(int)

    # # format the index to appear as dollar amounts
    rate_price_matrix.index = rate_price_matrix.index.map("${:,.0f}".format)

    # # format the values to appear as dollar amounts
    rate_price_matrix = rate_price_matrix.applymap("${:,.0f}".format)

    return rate_price_matrix


def cost_plot(max_list, rate_df):
    """This shows a bar chart of the total cost of the mortgage for different year options

    Args:
        max_list (list): A list of the maximum monthly payment, down payment, and interest rate.
        rate_df (DataFrame): A DataFrame of the interest rates and APRs.

    Returns:
        chart (altair.Chart): A bar chart of the total cost of the mortgage for different year options.
    """

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


def heat_map(r_p_matrix):
    """This shows a heat map of the total cost of the mortgage for different options"""

    r_p_matrix = r_p_matrix.copy()

    # convert the values to floats
    r_p_matrix = r_p_matrix.applymap(
        lambda x: float(x.replace("$", "").replace(",", ""))
    )

    # convert the index to floats
    r_p_matrix.index = r_p_matrix.index.map(
        lambda x: float(x.replace("$", "").replace(",", ""))
    )

    # extract the index and columns from the r_p_matrix
    x_ind = r_p_matrix.columns
    y_col = r_p_matrix.index

    z = r_p_matrix.values

    z_med = np.median(z)

    x, y = np.meshgrid(x_ind, y_col)

    # Convert this grid to columnar data expected by Altair
    source = pd.DataFrame({"Rate": x.ravel(), "Price": y.ravel(), "Payment": z.ravel()})

    heat_base = alt.Chart(source).encode(alt.Y("Price:O"), alt.X("Rate:O"))

    heat_map = heat_base.mark_rect().encode(alt.Color("Payment:Q"))

    heat_text = heat_base.mark_text(baseline="middle").encode(
        alt.Text("Payment:Q", format=".0f"),
        color=alt.condition(
            alt.datum.Payment < z_med, alt.value("black"), alt.value("white")
        ),
    )

    heat_chart = heat_map + heat_text

    return heat_chart
