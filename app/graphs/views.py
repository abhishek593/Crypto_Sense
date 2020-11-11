from flask import Blueprint, render_template, redirect, request, url_for, flash, abort, current_app, json
import time
import datetime
from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()

graphs_blueprint = Blueprint('graphs', __name__, template_folder='templates/graphs')


@graphs_blueprint.route('/g_main')
def home():
    return render_template('g_home.html')


@graphs_blueprint.route('/g_CoinCurrentPrice', methods=['POST', 'GET'])
def CoinCurrentPrice():
    if request.method == "POST":
        ids = (str)(request.form["id"])
        vs_currencies = (str)(request.form["vs_currencies"])
        include_last_update_date = (request.form["include_last_update_date"])
        include_24_hour_change = (request.form["include_24_hour_change"])
        include_market_cap = (request.form["include_market_cap"])
        data = cg.get_price(ids, vs_currencies, include_market_cap=include_market_cap,
                            include_last_updated_at=include_last_update_date,
                            include_24hour_change=include_24_hour_change)
        return render_template("g_CoinCurrentPrice_values.html", data=data)
    else:
        return render_template('g_CoinCurrentPrice.html')


@graphs_blueprint.route('/g_CoinHistoricalData1', methods=['POST', 'GET'])
def CoinHistoricalData1():
    if request.method == "POST":
        ids = request.form["id"]
        vs_currency = request.form["vs_currency"]
        days = (int)(request.form["days"])
        data = cg.get_coin_market_chart_by_id(ids, vs_currency, days)
        labels = []
        prices = []
        for val in data['prices']:
            labels.append(val[0])
            prices.append(val[1])

        market_cap = []
        for val in data['market_caps']:
            market_cap.append(val[1])

        total_volumes = []
        for val in data['total_volumes']:
            total_volumes.append(val[1])
        return render_template('g_CoinHistoricalData1_graph.html', prices=prices, market_cap=market_cap,
                               total_volumes=total_volumes, labels=labels)
    else:
        return render_template('g_CoinHistoricalData1.html')


@graphs_blueprint.route('/g_CoinHistoricalData2', methods=['POST', 'GET'])
def CoinHistoricalData2():
    if request.method == "POST":
        ids = request.form["id"]
        vs_currency = request.form["vs_currency"]
        from_time = (str)(request.form["from_time"])
        to_time = (str)(request.form["to_time"])
        from_time_unix = (int)(time.mktime(datetime.datetime.strptime(from_time, "%d/%m/%Y").timetuple()))
        to_time_unix = (int)(time.mktime(datetime.datetime.strptime(to_time, "%d/%m/%Y").timetuple()))
        data = cg.get_coin_market_chart_range_by_id(ids, vs_currency, from_time_unix, to_time_unix)
        labels = []
        prices = []
        for val in data['prices']:
            labels.append(val[0])
            prices.append(val[1])

        market_cap = []
        for val in data['market_caps']:
            market_cap.append(val[1])

        total_volumes = []
        for val in data['total_volumes']:
            total_volumes.append(val[1])

        return render_template('g_CoinHistoricalData2_graph.html', prices=prices, market_cap=market_cap,
                               total_volumes=total_volumes, labels=labels)
    else:
        return render_template('g_CoinHistoricalData2.html')


@graphs_blueprint.route('/g_CoinHistoryOnAParticularDate', methods=['POST', 'GET'])
def CoinHistoryOnAParticularDate():
    if request.method == "POST":
        ids = request.form["id"]
        date = request.form["date"]
        data = cg.get_coin_history_by_id(ids, date)["market_data"]
        labels = []
        prices = []
        market_cap = []
        for key, val in data['current_price'].items():
            labels.append(key)
            prices.append(val)

        market_cap = []
        for val in data['market_cap'].values():
            market_cap.append(val)

        return render_template('g_CoinHistoryOnAParticularDate_graph.html', prices=prices, market_cap=market_cap,
                               labels=labels)
    else:
        return render_template('g_CoinHistoryOnAParticularDate.html')


@graphs_blueprint.route('/g_CoinMarketData', methods=['POST', 'GET'])
def CoinMarketData():
    if request.method == "POST":
        id = request.form["id"]
        data = cg.get_coin_by_id(id)['market_data']
        val = data["market_cap_rank"]
        return render_template('g_CoinMarketData_value.html', value=val)
    else:
        return render_template('g_CoinMarketData.html')


@graphs_blueprint.route('/g_CoinsList')
def CoinsList():
    coins_list = cg.get_coins_list()
    return render_template('g_CoinsList.html', data=coins_list)


@graphs_blueprint.route('/g_SupportedTargetCurrencies')
def SupportedTargetCurrencies():
    data = cg.get_supported_vs_currencies()
    return render_template('g_SupportedTargetCurrencies.html', data=data)
