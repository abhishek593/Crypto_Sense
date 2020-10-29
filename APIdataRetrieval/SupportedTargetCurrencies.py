from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

# This just shows all the target currencies in which user can query
data = cg.get_supported_vs_currencies()
print(data)
