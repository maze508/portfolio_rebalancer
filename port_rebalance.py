from currency_converter import CurrencyConverter
import math
import numpy as np
import pandas as pd
from yahoo_fin import stock_info as si
import yfinance as yf
from tabulate import tabulate

from env import *


#! Checking Input Issues
def check_input(cash_total, target_asset_alloc):
    """Check issues in User inputs

    Args:
        cash_total (dict): Keys = cash injection, Values = currency of cash injection
        target_asset_alloc (dict): Keys = tickers, Values = target allocation(%) 

    Returns:
        [Bool]: True if everything is right
    """
    total_cash = list(cash_total.keys())
    cash_currency = list(cash_total.values())
    #* Ensure that lists are not empty
    if total_cash == [] or cash_currency == []:
        print('Please Enter a Valid Number for Cash Currency and Amount')
        return

    #* Ensure that length of both lists are the same
    if len(total_cash) != len(cash_currency):
        print('Please Ensure that the right amount/number of total cash/cash currency has been input')
        return

    #* Ensure target asset alloc is a dict
    assert type(target_asset_alloc) == dict, f'Target Asset Allocation should be in the form of a dictionary'

    #* Ensure that Target Asset Allocation adds up to 100%
    assert sum(target_asset_alloc.values()) == 100, f'Sum of Target Asset Allocation should add up to 100'

    assert sum(total_cash) >= 0, f'Sum of cash should be greater than 0'

    return True


#! Currency Conversion
def currency_conversion(cash_total):
    """Converts total cash injected into portfolio to USD

    Args:
        cash_total (dict): Keys = cash injection, Values = currency of cash injection

    Returns:
        sum_total_cash_in_usd [list]: total cash in USD
    """

    c = CurrencyConverter()
    cash_currency = list(cash_total.values())
    total_cash = list(cash_total.keys())
    #* Else ensure that all inputted currencies are in uppercase
    cash_currency = [i.upper() for i in cash_currency]

    #* Converts all cash currency to USD
    sum_total_cash_in_usd = []
    for i in range(len(cash_currency)):
        try: 
            sum_total_cash_in_usd.append(c.convert(total_cash[i], cash_currency[i], "USD"))
        except ValueError as error:
            print(error)
    sum_total_cash_in_usd = [sum(sum_total_cash_in_usd)]
    print()
    return sum_total_cash_in_usd


#! Portfolio Rebalancing
def port_rebalance(sum_total_cash_in_usd, target_asset_alloc, current_port):
    """[summary]

    Args:
        sum_total_cash_in_usd (list): total cash injection in USD
        current_port (dict) : Keys = tickers, Values = quantity of stocks
        target_asset_alloc (dict): Keys = tickers, Values = target allocation(%) 

    Returns:
        Multiple objects to be then displayed 
    """
    c = CurrencyConverter()

    current_asset_values = []
    indiv_share_price = []

    tickers = list(current_port.keys())
    quantity = list(current_port.values())

    #* Finds current asset values displayed in USD and individual stock prices
    for i in range(len(tickers)):

        # TODO : To Find a less Naive way to Solve this issue
        #! NOTE : Code here to ensure that prices of stocks are displayed in USD. However yfinance
        #! posts a series of API-ing issues
        try:
            currency_displayed = yf.Ticker(tickers[i]).info["currency"]
        except IndexError:
            print(f'Unable to Obtain Currency in which Ticker : [{tickers[i]}] is displayed in. Algorithm will assume it is displayed in [USD]')
            print()
        if currency_displayed != 'USD':
            stock_price = c.convert(si.get_live_price(tickers[i]), currency_displayed, "USD")
        else:
            stock_price = si.get_live_price(tickers[i])

        #! REPLACEMENT [To replace previous block of code if not working] : The Following Line is its current replacement without considering currency type at all 
        # stock_price = si.get_live_price(tickers[i])


        current_asset_values.append(stock_price * quantity[i])
        indiv_share_price.append(stock_price)
        si.get_live_price(tickers[i])
    current_asset_values = np.array(current_asset_values)
    indiv_share_price = np.array(indiv_share_price)

    #* Old Stock Allocation
    old_allocation = []
    sum_old_assets = sum(current_asset_values)
    for i in current_asset_values:
        old_allocation.append(round(i/sum_old_assets * 100, 2))
    total_new_assets = np.array(sum_old_assets + sum_total_cash_in_usd)

    #* Assets to buy and new asset values
    new_assets_values = total_new_assets * np.array(list(target_asset_alloc.values())) / 100
    assets_to_buy = new_assets_values - current_asset_values

    #* If Selling is Not Allowed. Revert the algorithm such that those stocks that were to be sold off initially to obtain best allocation
    #* is not sold and the amt of stocks to be bought is scaled down accordingly
    if not selling_allowed:
        temp_value = []
        # Sets all negative values to 0
        for i in range(len(assets_to_buy)):
            if assets_to_buy[i] < 0:
                temp_value.append(abs(assets_to_buy[i]))
                assets_to_buy[i] = 0
        # Finds the sum of all these negative values that were set to 0 in the previuos for loop such that the 'extra money' is accounted for
        temp_value = sum(temp_value)
        # Adjust the New total asset values after considering no selling of stocks
        new_total_assets = total_new_assets - temp_value
        over_val_sum = sum(assets_to_buy)
        # Adjusting new total assets to buy values accordingly after considering no selling of stocks
        for counter in range(len(assets_to_buy)):
            if assets_to_buy[counter] != 0:
                assets_to_buy[counter] = assets_to_buy[counter] / over_val_sum * sum_total_cash_in_usd[0]
    
    #* No. of New units to buy
    units_to_buy = []
    for i in range(len(assets_to_buy)):
        #! Note that math.floor can only be performed on 1 value, thus the for loop
        amt_to_buy = math.floor(assets_to_buy[i] / indiv_share_price[i])
        units_to_buy.append(amt_to_buy)
    units_to_buy = np.array(units_to_buy)
    price_of_units_to_buy = units_to_buy * indiv_share_price

    #* New Allocation
    quantities_array = np.array(quantity)
    current_quantity = quantities_array + units_to_buy
    current_portfolio_values = current_quantity * indiv_share_price
    current_portfolio_worth = sum(current_portfolio_values)

    for i in current_portfolio_values:
        new_allocation = current_portfolio_values / current_portfolio_worth

    #* Largest Discrepancy between new and target allocations
    target_alloc = np.array(list(target_asset_alloc.values()))
    largest_discrepancy = round(max(abs(target_alloc - (new_allocation * 100))), 2)

    #* New Quantities of Stocks in Portfolio
    final_quantity = quantities_array + units_to_buy

    #* Cash Spent and Remaining Cash
    cash_spent = round(sum(units_to_buy * indiv_share_price), 2)
    cash_remaining = round(sum_total_cash_in_usd[0] - sum(units_to_buy * indiv_share_price), 2)

    return indiv_share_price, current_asset_values, old_allocation, new_assets_values, assets_to_buy, units_to_buy, price_of_units_to_buy, final_quantity, current_portfolio_worth, current_portfolio_values, new_allocation, largest_discrepancy, cash_spent, cash_remaining, target_alloc


#! Generate Report
def generate_report(sum_total_cash_in_usd, current_port, indiv_share_price, current_asset_values, old_allocation, new_assets_values, assets_to_buy, units_to_buy, price_of_units_to_buy, final_quantity, current_portfolio_worth, current_portfolio_values, new_allocation, largest_discrepancy, cash_spent, cash_remaining, target_alloc):
    """
        Generates Report
    """
    quantities = list(current_port.values())
    tickers = list(current_port.keys())

    #* Dataframe Generating to Display Data
    df = pd.DataFrame()
    df['Current Price' + '\n' + '[USD]'] = [round(i, 2) for i in indiv_share_price]
    df['Initial Quantities'] = quantities 
    df['Initial Stock Values' + '\n' + ' [USD]'] = [round(i, 2) for i in current_asset_values]
    df['Old Allocation' + '\n' + ' (%)'] = old_allocation
    df['No. of Units to Buy'] = units_to_buy
    df['Price of Stocks to Buy' + '\n' + ' [USD]'] = [round(i, 2) for i in price_of_units_to_buy]
    df['Final Quantity'] = final_quantity
    df['Final Allocation' + '\n' + ' (%)'] = [round(i, 2) for i in new_allocation * 100]
    df['Target Allocation' + '\n' + ' (%)'] = [round(i, 2) for i in target_alloc]

    #* Change name of index
    print(tickers)
    for i, x in enumerate(df.index):
        df.rename(index={x : tickers[i]}, inplace=True)
    

    print()
    print("\033[1m" + "Cash Details :" + "\033[0m")
    print()
    print("Total Cash Injection in [USD] :", round(sum_total_cash_in_usd[0], 2))
    print(f'Used Cash : {cash_spent} USD')
    print(f'Leftover Cash : {cash_remaining} USD')

    print("\n")

    print("\033[1m" + "Tabular Data :" + "\033[0m")
    print()
    print(tabulate(df, headers='keys', tablefmt="fancy_grid"))

    print("\n")

    print("\033[1m" + "Portfolio Allocation Details :" + "\033[0m")
    print()
    print(f'Largest Deviation of Final Allocation Observed : {largest_discrepancy} %')
    print("\n")

    return df