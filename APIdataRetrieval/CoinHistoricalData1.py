from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

print("Here you can get the coin historical data.")
id = input("Enter the coin name - ")
vs_currency = input("Enter the target currency. Eg - inr, usd - ")
days = input("Enter the number of days - ")
data = cg.get_coin_market_chart_by_id(id, vs_currency, days)

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
