from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()
import time
import datetime


# The below is another version of getting coin historical data where a user can enter the timestamp i.e,
# from date to to_data

print("Here you can get the coin historical data.")
id = input("Enter the coin name - ")
vs_currency = input("Enter the target currency. Eg - inr, usd - ")
from_time = input('Enter the starting date in format dd/mm/yyyy: ')
to_time = input('Enter the ending date in format dd/mm/yyyy: ')
from_time_unix = time.mktime(datetime.datetime.strptime(from_time, "%d/%m/%Y").timetuple())
to_time_unix = time.mktime(datetime.datetime.strptime(to_time, "%d/%m/%Y").timetuple())

data = cg.get_coin_market_chart_range_by_id(id, vs_currency, from_time_unix, to_time_unix)

# Same thing needs to be done here as in the 1st version
# Just copying here so one doesn't need to switch

# Each of the prices, market_cap, total_volumes is an jsonArray
# Each object in this jsonArray contains two piece of information and their are several objects in 1 JsonArray
# First is value for id(as above) and other is vs_currency(target-currency)
# We want 3 graphs
# First graph is for prices Y axis contains id and X axis contains vs_currency
# Example = if I want prices from bitcoin to inr
# id = bitcoin and vs_currency = inr
# So for all objects I want bitcoin on Y axis and inr on X axis
# So total will be 3 graphs
prices = data['prices']
market_cap = data['market_cap']
total_volumes = data['total_volumes']

