"""This module get the interest rates from mortgagereports.com"""

import pandas as pd


def get_rates():

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
