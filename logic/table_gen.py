"""This module calculates the table of affordability."""

import pandas as pd


def mortgage_cost(principal, rate, term):
    """This function calculates the cost of a mortgage."""

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


def rate_afford_table(int_rate, down_pmt, term, price):
    """This function calculates the table of affordability."""

    # Create a table of affordability

    # Initialize the table
    rate_afford_table = pd.DataFrame(
        columns=[
            "Rate",
            "Payment",
            "Principal",
            "Interest",
            "Total Cost",
        ]
    )

    # fill the Rate column with sample interest rates 2% to 10% in .25% increments
    rate_afford_table["Rate"] = [x for x in range(200, 1100, 25)]
    rate_afford_table["Rate"] = rate_afford_table["Rate"] / 100

    # add the int_rate to the table and sort the table
    rate_afford_table.loc[len(rate_afford_table.index)] = [int_rate, 0, 0, 0, 0]
    rate_afford_table = rate_afford_table.sort_values(by="Rate")
    rate_afford_table.reset_index(drop=True, inplace=True)

    # filter the table for int_rate +/- 3
    rate_afford_table = rate_afford_table[
        (rate_afford_table["Rate"] >= int_rate - 3)
        & (rate_afford_table["Rate"] <= int_rate + 3)
    ]

    # fill the principal column with the price - down_pmt
    rate_afford_table["Principal"] = price - down_pmt

    # fill the Payment, Interest, and Total Cost columns with the mortgage_cost function
    (
        rate_afford_table["Payment"],
        rate_afford_table["Total Cost"],
        rate_afford_table["Interest"],
    ) = zip(
        *rate_afford_table.apply(
            lambda x: mortgage_cost(x["Principal"], x["Rate"], term), axis=1
        )
    )

    # round the table to 2 decimal places
    rate_afford_table = rate_afford_table.round(2)

    return rate_afford_table


def price_afford_table(int_rate, down_pmt, term, price):
    """This function calculates the table of affordability."""

    # Create a table of affordability

    # Initialize the table
    price_afford_table = pd.DataFrame(
        columns=[
            "Price",
            "Payment",
            "Principal",
            "Interest",
            "Total Cost",
        ]
    )

    # fill the Price column with sample prices +/- 25% of the Price in 5% increments
    price_minus = price - (price * 0.25)
    price_plus = price + (price * 0.25)
    price_afford_table["Price"] = [
        x for x in range(int(price_minus), int(price_plus), int(price * 0.05))
    ]

    # fill the principal column with the price - down_pmt
    price_afford_table["Principal"] = price_afford_table["Price"] - down_pmt

    # fill the Payment, Interest, and Total Cost columns with the mortgage_cost function
    (
        price_afford_table["Payment"],
        price_afford_table["Total Cost"],
        price_afford_table["Interest"],
    ) = zip(
        *price_afford_table.apply(
            lambda x: mortgage_cost(x["Principal"], int_rate, term), axis=1
        )
    )

    # round the table to 2 decimal places
    price_afford_table = price_afford_table.round(2)

    return price_afford_table
