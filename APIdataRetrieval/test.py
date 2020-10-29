from pycoingecko import CoinGeckoAPI
import json
cg = CoinGeckoAPI()

# For fetching list of supported currencies
# supported_currencies = cg.get_supported_vs_currencies()
# coins_list = cg.get_coins_list()
# ans = []
# for curr in supported_currencies:
#     for coin in coins_list:
#         if curr == coin['symbol']:
#             ans.append({
#                 'id': coin['id'],
#                 'symbol': curr,
#                 'coin_name': coin['name']
#             })
# with open('coins.json', 'w') as f:
#     json.dump(ans, f)
# print(ans)


from app.models import UserProfile, Investment, Transaction
from app import db
# user = UserProfile(username='abhi593', email='abhi@gmail.com', first_name='Abhishek', last_name='Bansal', password='abhishek')
# db.session.add(user)
# db.session.commit()
# inv1 = Investment(user_id=user.id, coin_name='btc', number_of_coins=10, total_price=100)
# db.session.add(inv1)
# db.session.commit()
# trans1 = Transaction(investment_id=inv1.id, coin_name='btc', number_of_coins=10, total_price=100)
# db.session.add(trans1)
# db.session.commit()


with open('coins.json') as f:
    supported_currencies = json.load(f)
coins_list = []
for curr in supported_currencies:
    coins_list.append(curr['id'])
# print(coins_list)
prices = cg.get_price(ids=coins_list, vs_currencies='usd')
print(prices)
for curr in supported_currencies:
    curr['price'] = prices[curr['id']]['usd']
print(supported_currencies)