from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

# This gives the historical data of a coin on a particular day
# i.e, we want to plot the data of this coin like market_cap or price with other available coins

print("Here you can get the coin historical data on a particular day.")
id = input("Enter the coin name - ")
date = input("Enter the day on which you want the historical data of this coin in the dd-mm-yyyy format: ")

data = cg.get_coin_history_by_id(id, date)

# Example -
# if I want to compare bitcoin with all other coins I will enter id as bitcoin
# For plotting price this value will be in Y axis and other coins will be on X axis
# Their will be bar charts arising from each of these coins
# The data is stored in prices and market_cap list

prices = data['prices']
market_cap = data['market_cap']

# For each of this you can see first element is coin name and other is conversion price or market_data
