# Rebalance-Crypto

Places limit buys and stop-loss sells of cryptoassets in order to rebalance a portfolio to a baseline percentage allocation. 

Download python https://www.python.org/downloads/
Download Visual C++ build tools: http://landinghub.visualstudio.com/visual-cpp-build-tools
Run pip install python-binance

API Used: https://github.com/sammchardy/python-binance

1. Adjust "api_key" and "api_secret" to your Binance API key/secret

2. Add coin tickers to "target_coins"

3. Add percentage allocations in decimal to "target_splits"

3a. Allocations for any coins found in "target_coins", but not in "target_splits" will be evenly split using the remaining percentage left 
over from the "target_splits" total 

3b. Leave total_splits<=1

4. All buys/sells/pricing is through BTC

5. Buys/sells are placed at the limit spread set in "price". Default is 1%.

6. Running the script will remove any pending buys and sells in your account!

7. When the script runs, buys/sells will be placed at the limits set in "price" until the percentages equal the allocation in "target_split"
