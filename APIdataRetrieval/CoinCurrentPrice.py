from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

# This gives the current price of any coin into any number of other coins

print('This gives the current price of any cryptocurrency(ies), into any number of target currency(ies). - ')
ids = input("Enter the coin name(If multiple separate by commas.Eg - bitcoin, ehtereum) : ")
vs_currencies = input('Enter the target currencies. If multiple - separate by commas. Eg - inr, usd')
include_last_update_date = int(input("Enter 1 if want to include last updated date else enter 0"))
include_24_hour_change = int(input("Enter 1 if want to include change in last 24 hours else enter 0"))
include_market_cap = int(input("Enter 1 if want to include market cap of coin  else enter 0"))

data = cg.get_price(ids, vs_currencies, include_market_cap=include_market_cap,
                    include_last_updated_at=include_last_update_date, include_24hour_change=include_24_hour_change)

print(data)
# We don't have to generate any charts here
# This will be directly displayed to user.
