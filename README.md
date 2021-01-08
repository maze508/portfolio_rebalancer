# Portfolio Balancer

[![Documentation Status](https://readthedocs.org/projects/ansicolortags/badge/?version=latest)](http://ansicolortags.readthedocs.io/?badge=latest) [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)      [![made-for-VSCode](https://img.shields.io/badge/Made%20for-VSCode-1f425f.svg)](https://code.visualstudio.com/)


A simple algorithm that helps you split your assets quickly into their pre - specified allocations 


***Rebalancing Portfolio has never been so easy***

![](images/its_easy.png)

## Installation
***
<br>

- Download Repository

        git clone https://github.com/maze508/portfolio_rebalancer.git

- Navigate to correct directory

        cd port_balancer

- Install Relevant Packages

        pip install -r requirements.txt


## How to Use
***
<br>

Open the `env.py` file and define the following fields

    total_cash         - Total Cash Injection
    cash_currency      - Currency type of Cash Injection
    tickers            - Ticker Symbol of Investment Instrument
    quantities         - Quantities of Corresponding Investment Instrument
    target_asset_alloc - Target Asset Allocation (%)

    [Optional] selling_allowed - Allow or Disallow Algorithm to sell owned assets

Run `main.py` 


## Demo
***

Below is a possible portfolio composition

```python
total_cash = [30000, 500] 

cash_currency = ['usd', 'sgd']

tickers = [
    "TSLA",
    "NIO",
    "XPEV",
    "LI"
]

quantities = [4,20,50,100]

target_asset_alloc = {
    "TSLA": 20,
    "NIO": 20,
    "XPEV": 40,
    "LI": 20
}

selling_allowed = False

```

After running `main.py` the resulting terminal display / output should be close to the following

![](images/portfolio_rebalancer_output.png)

## Road Map
***

- [ ] More Flexible Currency Conversion 
- [ ] Increase Calculating Speed (Optimisation)
- [x] Detailed Documentation

## References

> Images
>> its_easy.png - http://www.andyhanselman.com/2016/07/08/improving-your-customer-experience-with-technology-its-easy/
