from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

print("This shows the coin's market data.")
id = input("Enter the coin name - ")
data = cg.get_coin_by_id(id)['market_data']
print(id + 'coin current rank = ' + str(data['market_cap_rank']))

