"""This module calculates the table of affordability."""

import pandas as pd
import numpy_financial as npf


def max_cost(max_pay, max_down, max_rate, term):
    """This function calculates the maximum purchase price."""

    # Calculate the maximum purchase price using pv
    max_price = npf.pv(max_rate / 100 / 12, term * 12, max_pay, when="begin")

    # Calculate the maximum principal
    max_total = max_price - max_down

    return abs(max_total)


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


def build_rate_price_matrix(int_rate, pay_price, down_payment):
    """This function builds a matrix of affordability."""

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

    # # make a payment list with the computed payment for each rate/price combo
    # payment_list = []
    # for rate in rate_list:
    #     for price in price_list:
    #         payment_list.append(mortgage_cost(price - down_payment, rate, 30)[0])

    # rate_price_matrix = pd.DataFrame(
    #     {"x": rate_list.ravel(), "y": price_list.ravel(), "z": payment_list.ravel()}
    # )

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
