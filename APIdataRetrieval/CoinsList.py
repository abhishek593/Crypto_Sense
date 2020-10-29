from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

# As the name suggests this gives all the lists of coins
# But this only contains coin id , it's symbol(a way of representing, we don't need it), and name of coin
# No graph needed
coins_list = cg.get_coins_list()
print(coins_list)
