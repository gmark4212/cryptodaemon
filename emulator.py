#!/usr/bin/python
# -*- coding: utf-8 -*-

from config import *


class MockExchange:
    def __init__(self):
        self.orders = []
        self.order_id = 1
        self.balance = FAKE_BALANCE


    def fetch_balance(self):# Текущий баланс
        balance ={'info': [{'currency': 'BTC', 'available': '{}'.format(self.balance), 'reserved': '1'}, {'currency': 'VERI', 'available': '20', 'reserved': '1'}, {'currency': 'LTC', 'available': '10', 'reserved': '1'}]}
        return  balance

    def fetch_ticker(self,pair):#запрос курса валюты
        pair = DEFAULT_EXCHANGE.fetch_ticker(pair)
        return pair

    def fetch_open_orders(self,pair = None):#проверка отокрытых ордеров
        orders = self.orders
        if pair:
            orders = []
            for order in self.orders:
                if order['symbol'] == pair:
                    orders.append(order)
        return orders

    def fetch_order(self,id):#Текущий ордер
        responce = ' order {} not found'.format(id)
        for order in self.orders:
            if order['id'] == id:
                responce = order
        return responce


    def create_order(self, symbol, typer, side, amount, price=None, params={}):#Создание ордера
        order ={
            'id': self.order_id,
            'timestamp': 1528460077870,
            'datetime':  '2018-06-08T12:14:38.870Z',
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
        return order

e = MockExchange()
print(e.fetch_ticker('VERI/BTC'))