#!/usr/bin/python
# -*- coding: utf-8 -*-

from config import *


class MockExchange:
    def __init__(self):
        self.orders = []
        self.order_id = 1


    def fetch_balance(self):# Текущий баланс
        balance ={'info': [{'currency': 'BTC', 'available': '0.10', 'reserved': '1'}, {'currency': 'VERI', 'available': '20', 'reserved': '1'}, {'currency': 'LTC', 'available': '10', 'reserved': '1'}]}
        return  balance

    def fetch_ticker(self,pair):#запрос курса валюты
        pair ={'symbol': pair, 'timestamp': 1528460077870, 'datetime': '2018-06-08T12:14:38.870Z', 'high': 0.011289, 'low': 0.009199, 'bid': 0.00965, 'bidVolume': None, 'ask': 0.009746, 'askVolume': None, 'vwap': 0.010367909770867987, 'open': 0.010514, 'close': 0.009746, 'last': 0.009746, 'previousClose': None, 'change': -0.0007680000000000013, 'percentage': -7.304546319193468, 'average': 0.01013, 'baseVolume': 1234.834, 'quoteVolume': 12.802647494, 'info': {'ask': '0.009746', 'bid': '0.009650', 'last': '0.009746', 'open': '0.010514', 'low': '0.009199', 'high': '0.011289', 'volume': '1234.834', 'volumeQuote': '12.802647494', 'timestamp': '2018-06-08T12:14:37.870Z', 'symbol': 'VERIBTC'}}
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