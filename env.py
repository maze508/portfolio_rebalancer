total_cash = [30000, 500] 

# Currency type of Cash Injection [list]
cash_currency = ['usd', 'sgd']

# Ticker Symbol of Investment Instrument [list]
tickers = [
    "TSLA",
    "NIO",
    "XPEV",
    "LI"
]

# Quantities of Corresponding Investment Instrument [list]
quantities = [4,20,50,100]

# Target Asset Allocation (%) [dict : (Keys --> ticker) (Values --> % Allocation)]
target_asset_alloc = {
    "TSLA": 20,
    "NIO": 20,
    "XPEV": 40,
    "LI": 20
}

# Flag to allow or disallow selling [(Bool) : `True OR False`]
selling_allowed = False