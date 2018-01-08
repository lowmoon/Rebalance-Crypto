from binance.client import Client

api_key = 'pub'
api_secret = 'secret'

print('connecting..')

client = Client(api_key, api_secret)


for order in client.get_open_orders():
    client.cancel_order(orderId=order['orderId'], symbol=order['symbol'])


target_coins = ['ETH', 'XLM', 'KNC', 'SALT', 'NEO',
    'POWR', 'ENG', 'EOS', 'REQ', 'QTUM', 'QSP', 'VEN', 'NEBL', 'OMG']


target_splits = {'ETH': .05, 'NEO' : .2, 'VEN': .01, 'POE': .05, 'XLM': .05}

missing_coins = [x for x in target_coins if not x in target_splits]

remaining_allocation = 1 - sum(target_splits.values())

for coin in missing_coins:
    target_splits[coin] = remaining_allocation / len(missing_coins)

print("splits as follows")
for split in target_splits:
    print(split + ": " + str(target_splits[split]))

print('getting prices..')
prices = {x['symbol']: float(x['price']) for x in client.get_all_tickers()}
print('getting account balances..')
current_distributions = {x: float(client.get_asset_balance(x)['free']) for x in target_coins}
current_distributions_base_btc = {x: prices[x+ 'BTC'] * current_distributions[x] for x in target_coins}

btc_stored = float(client.get_asset_balance('BTC')['free'])
altcoin_value_btc = sum(current_distributions_base_btc.values())

total_value = btc_stored + altcoin_value_btc
altcoin_target_value = total_value * .9

btc_price = prices['BTCUSDT']
print('total account value: ' + str(total_value) + ' btc ($' + str(total_value * btc_price) + ')')

current_splits = {x: current_distributions_base_btc[x]/altcoin_target_value for x in target_coins}
deltas_pct = {x: target_splits[x] - current_splits[x] for x in target_coins}

print('portfolio delta:')

from math import log10, floor
def round_sig(x, sig=2):
    return round(x, sig-int(floor(log10(abs(x))))-1)
client.get_open_orders()
for c in target_coins:
    btc_symbol = c + 'BTC'
    target_amount = target_splits[c] * altcoin_target_value/prices[btc_symbol]
    actual_amount = current_distributions[c]
    delta = round_sig(target_amount - actual_amount, 3)
    print(c + ': ' + str(delta))
    price = '{0:f}'.format(round_sig(prices[btc_symbol] * (.99 if delta > 0 else 1.01),3))
    print('price: ' + str(price))
    try:
        order = client.create_order(
            symbol=btc_symbol,
            side = Client.SIDE_BUY if delta > 0 else Client.SIDE_SELL,
            type = Client.ORDER_TYPE_LIMIT,
            quantity=abs(delta),
            price = price,
            timeInForce='GTC')
    except:
        print('error with order')
        continue
