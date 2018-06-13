#!/usr/bin/python
# -*- coding: utf-8 -*-

from config import *

class MockExchange:
    def __init__(self):
        self.orders = []
        self.order_id = 1
        self.trade_id = 1
        self.balance = FAKE_BALANCE
        self.trades = []

    def fetch_balance(self): # Текущий баланс
        balance = {'info': [{'currency': BASE_TICKER, 'available': '{}'.format(self.balance), 'reserved': '1'}, {'currency': 'VERI', 'available': '20', 'reserved': '1'}, {'currency': 'LTC', 'available': '10', 'reserved': '1'}]}
        return balance

    def fetch_ticker(self,pair): # запрос курса валюты
        pair = DEFAULT_EXCHANGE.fetch_ticker(pair)
        return pair

    def fetch_open_orders(self,pair = None): # проверка открытых ордеров
        for order in self.orders:
            self.find_same_trades(order)
        orders = self.orders
        if pair:
            orders = []
            for order in self.orders:
                if order['symbol'] == pair:
                    orders.append(order)
        return orders

    def fetch_order(self, id): # Текущий ордер
        responce = ' order {} not found'.format(id)
        for order in self.orders:
            if order['id'] == id:
                self.find_same_trades(order)
                responce = order
        return responce


    def create_order(self, symbol, typer, side, amount, price=None, params={}): # Создание ордера
        date = self.fetch_ticker('LTC/BTC') # Запрос для получуния метки времени с биржи
        order = {
            'id': self.order_id,
            'timestamp': date['timestamp'],
            'datetime':  date['datetime'],
            'lastTradeTimestamp': None,
            'status': 'open',
            'symbol': symbol,
            'type': typer,
            'side': side,
            'price': price,
            'amount': amount,
            'cost': None,
            'filled': 0,
            'remaining': amount,
            'fee': None,
            'info': None,
        }
        self.orders.append(order)
        self.order_id += 1
        print(order)
        return order

    def fetch_bid_orders(self,pair): # Ордера на покупку [сумма : количество]
        info = DEFAULT_EXCHANGE.fetchOrderBook(pair)
        return info['bids']

    def fetch_ask_orders(self,pair): # Ордера на продажу [сумма : количество]
        info = DEFAULT_EXCHANGE.fetchOrderBook(pair)
        return info['asks']

    def fetch_last_trades(self,pair): # Последние совершенные сделки
        info = DEFAULT_EXCHANGE.fetchTrades(pair)
        return info

    def fetch_my_trades(self): # Просммотр всех своих сделок
        trades = self.trades
        return trades



    def add_trade(self, trade, order): # Создание сделки
        trade['price'] = order[ 'price']
        trade['cost'] = float(trade['price']) * float(trade['amount'])
        order['timestamp'] = trade['timestamp'] # Обновление метки времени ордера
        # trade['info']['price'] параметр оригинальной сделки trade['price'] параметр сделки эмулятора
        order['remaining'] = round(order['remaining'],14) # округление до 14 знаков после запятой
        # print('куплю',trade['amount'])
        # print('от',order['remaining'])
        if float(trade['amount']) >= float(order['remaining']):
            # print('покупаю весь ордер')
            trade['amount'] = float(order['remaining'])
            order['filled'] = order['amount']
            order['remaining'] = 0
            order['status'] = 'filled'
        else:
            # print('покупаю часть')
            # print(order['remaining'],'-',trade['amount'])
            order['remaining'] = float(order['remaining']) - float(trade['amount'])
            # print(order['remaining'])
            # print(order['filled'], '+', trade['amount'])
            order['filled'] = float(order['filled']) + float(trade['amount'])
            # print(order['filled'])
        print(trade)
        self.trades.append(trade)


    def find_same_trades(self,order):
        trades = self.fetch_last_trades(order['symbol'])
        for trade in trades:
            if order['status'] == 'open':
                if trade['side'] == order['side']:
                    if float(trade['price']) >= float(order['price']):
                        # self.add_trade(trade, order) # Если проверять сделки за сутки
                        if int(trade['timestamp']) > int(order['timestamp']):
                            self.add_trade(trade, order)
            else:
                break

if __name__ =='__main__':
    e = MockExchange()
    order = e.create_order('LTC/BTC','stopLimit','buy',5,0.015)
    e.find_same_trades(order)
    print(order)