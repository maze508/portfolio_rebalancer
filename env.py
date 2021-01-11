# Details of Cash Injection [dict : (Keys --> amount of cash injection) (Values --> currency of cash injection)]
cash_total = {
    30000: 'usd',
    500: 'sgd'
}

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