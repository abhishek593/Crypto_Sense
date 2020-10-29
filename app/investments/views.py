from flask import Blueprint, render_template, redirect, request, url_for, flash, abort, current_app
from flask_login import login_user, login_required, logout_user, current_user
from app.models import UserProfile, Investment, Transaction
import json
from app.models import UserProfile
from app import db
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

investments_blueprint = Blueprint('investments', __name__, template_folder='templates/investments')


@investments_blueprint.route('/<username>/dashboard')
@login_required
def dashboard(username):
    user = UserProfile.query.filter_by(username=username)
    if user is not None:
        user = user.first()
        user_coin_investments_list = user.coin_investments
        return render_template('dashboard.html', user_coin_investments_list=user_coin_investments_list, user=user)
    else:
        return render_template('404_error')


@investments_blueprint.route('/<username>/purchase', methods=['GET', 'POST'])
@login_required
def purchase(username):
    user = UserProfile.query.filter_by(username=username)
    if user is not None:
        user = user.first()
        coin_name = request.form['coin_name']
        coin_conversion_rate = float(request.form['coin_conversion_rate'])
        purchase_amount = float(request.form['purchase_amount'])
        if purchase_amount <= user.balance:
            number_of_coins = purchase_amount / coin_conversion_rate
            coin_investment_instance = None
            for coin in user.coin_investments:
                if coin.coin_name == coin_name:
                    coin_investment_instance = coin
                    break
            if coin_investment_instance is None:
                coin_investment_instance = Investment(user_id=user.id, coin_name=coin_name,
                                                      number_of_coins=number_of_coins, total_price=purchase_amount)
            else:
                coin_investment_instance.number_of_coins += number_of_coins
                coin_investment_instance.total_price += purchase_amount
            db.session.add(coin_investment_instance)
            db.session.commit()
            transaction = Transaction(investment_id=coin_investment_instance.id, coin_name=coin_name,
                                      number_of_coins=number_of_coins, total_price=purchase_amount)
            db.session.add(transaction)
            db.session.commit()
            user.balance -= purchase_amount
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('investments.dashboard', username=user.username))
        else:
            flash("Insufficient balance.")
            return redirect(url_for('investments.checkprice', username=user.username))
    else:
        return render_template('404_error')


@investments_blueprint.route('/<username>/checkprice')
@login_required
def checkprice(username):
    user = UserProfile.query.filter_by(username=username)
    if user is not None:
        user = user.first()
        with open('app/investments/coins.json') as f:
            supported_currencies = json.load(f)
        coins_list = []
        for curr in supported_currencies:
            coins_list.append(curr['id'])
        prices = cg.get_price(ids=coins_list, vs_currencies='usd')
        for curr in supported_currencies:
            curr['price'] = prices[curr['id']]['usd']
        return render_template('checkprice.html', supported_currencies=supported_currencies)
    else:
        return render_template('404_error.html')


@investments_blueprint.route('/<username>/sell')
@login_required
def sell(username):
    user = UserProfile.query.filter_by(username=username)
    if user is not None:
        user = user.first()
        coins_list = []
        user_coin_investments = user.coin_investments
        for coin in user_coin_investments:
            if coin.number_of_coins > 0:
                coins_list.append(coin.coin_name)
        prices = cg.get_price(ids=coins_list, vs_currencies='usd')
        sell_coins_list = []
        with open('app/investments/coins.json') as f:
            supported_currencies = json.load(f)
        for coin in coins_list:
            for item in supported_currencies:
                if coin == item['id']:
                    obj = item
                    obj['current_price'] = prices[item['id']]['usd']
                    coin_instance = None
                    for c in user_coin_investments:
                        if coin == c.coin_name:
                            coin_instance = c
                            break
                    obj['current_holding'] = coin_instance.total_price
                    obj['number_of_coins'] = coin_instance.number_of_coins
                    sell_coins_list.append(obj)
        return render_template('sell.html', sell_coins_list=sell_coins_list)
    else:
        return render_template('404_error')


@investments_blueprint.route('/<username>/confirm_sell', methods=['GET', 'POST'])
@login_required
def confirm_sell(username):
    user = UserProfile.query.filter_by(username=username)
    if user is not None:
        user = user.first()
        coin_name = request.form['coin_name']
        coin_conversion_rate = float(request.form['coin_conversion_rate'])
        sell_amount = float(request.form['sell_amount'])

        if coin_name is None or coin_conversion_rate is None or sell_amount is None:
            return redirect(url_for('investments.sell', username=user.username))
        number_of_coins = sell_amount / coin_conversion_rate
        coin_investment_instance = None
        for coin in user.coin_investments:
            if coin.coin_name == coin_name:
                coin_investment_instance = coin
                break
        success = False
        if coin_investment_instance is None:
            flash("You don't have any holdings of this coin.")
        else:
            if coin_investment_instance.total_price >= sell_amount:
                coin_investment_instance.number_of_coins -= number_of_coins
                coin_investment_instance.total_price -= sell_amount
                db.session.add(coin_investment_instance)
                db.session.commit()
                transaction = Transaction(investment_id=coin_investment_instance.id, coin_name=coin_name,
                                          number_of_coins=number_of_coins, total_price=sell_amount)
                db.session.add(transaction)
                db.session.commit()
                user.balance += sell_amount
                db.session.add(user)
                db.session.commit()
                success = True
        return render_template('confirm_sell.html', success=success)
    else:
        return render_template('404_error')
