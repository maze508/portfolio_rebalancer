from env import *
from port_rebalance import *


# Run this function after configuring env.py
def main():
    if not check_input(cash_total, target_asset_alloc):
        raise Exception('Please Fix Input Errors before continuing')

    sum_total_cash_in_usd = currency_conversion(cash_total)
    indiv_share_price, current_asset_values, old_allocation, new_assets_values, assets_to_buy, units_to_buy, price_of_units_to_buy, final_quantity, current_portfolio_worth, current_portfolio_values, new_allocation, largest_discrepancy, cash_spent, cash_remaining, target_alloc = port_rebalance(sum_total_cash_in_usd, target_asset_alloc, current_port)
    generate_report(sum_total_cash_in_usd, current_port, indiv_share_price, current_asset_values, old_allocation, new_assets_values, assets_to_buy, units_to_buy, price_of_units_to_buy, final_quantity, current_portfolio_worth, current_portfolio_values, new_allocation, largest_discrepancy, cash_spent, cash_remaining, target_alloc)


if __name__ == '__main__':
    main()