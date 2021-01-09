# Amount of total Cash Injection [list]
total_cash = [30000, 500] 

# Currency type of Cash Injection [list]
cash_currency = ['usd', 'sgd']

# Current Portfolio Composition [dict : (Keys --> tickers) (Values --> Quantity of stock)]
current_port = {
    "TSLA": 4,
    "NIO": 20,
    "XPEV": 50,
    "LI": 100
}


# Target Asset Allocation (%) [dict : (Keys --> ticker) (Values --> % Allocation)]
target_asset_alloc = {
    "TSLA": 20,
    "NIO": 20,
    "XPEV": 40,
    "LI": 20
}

# Flag to allow or disallow selling [(Bool) : `True OR False`]
selling_allowed = False