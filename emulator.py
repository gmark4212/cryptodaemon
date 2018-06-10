#!/usr/bin/python
# -*- coding: utf-8 -*-

from config import *
import random

class MockExchange:
    def __init__(self):
        self.orders = []
        self.order_id = 1
        self.trade_id = 1
        self.balance = FAKE_BALANCE
        self.trades = []

    def fetch_balance(self):# Текущий баланс
        balance ={'info': [{'currency': 'BTC', 'available': '{}'.format(self.balance), 'reserved': '1'}, {'currency': 'VERI', 'available': '20', 'reserved': '1'}, {'currency': 'LTC', 'available': '10', 'reserved': '1'}]}
        return  balance

    def fetch_ticker(self,pair): # запрос курса валюты
        pair = DEFAULT_EXCHANGE.fetch_ticker(pair)
        return pair

    def fetch_open_orders(self,pair = None): # проверка открытых ордеров
        for order in self.orders:
            self.trade(order)
        orders = self.orders
        if pair:
            orders = []
            for order in self.orders:
                if order['symbol'] == pair:
                    orders.append(order)
        return orders

    def fetch_order(self,id): # Текущий ордер
        responce = ' order {} not found'.format(id)
        for order in self.orders:
            if order['id'] == id:
                self.trade(order)
                responce = order
        return responce


    def create_order(self, symbol, typer, side, amount, price=None, params={}):# Создание ордера
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

    def fetch_bid_orders(self,pair): # Ордера на покупку [сумма : количество]
        info = DEFAULT_EXCHANGE.fetchOrderBook(pair)
        return info['bids']

    def fetch_ask_orders(self,pair): # Ордера на продажу [сумма : количество]
        info = DEFAULT_EXCHANGE.fetchOrderBook(pair)
        return info['asks']

    def fetch_last_trades(self,pair): # Последние совершенные сделки
        info = DEFAULT_EXCHANGE.exchange.fetchTrades(pair)
        return info

    def fetch_my_trades(self):# Просммотр всех своих сделок
        trades = self.trades
        return trades


    def trade(self,order):#Эмуляция торговли
        piece = random.choice([0,0.5,1])
        if piece !=0:
            order['filled'] = order['remaining']*piece
            order['remaining']-=order['filled']
            if order['remaining']== 0:
                order['status']='filled'
            self.add_trade(order['price']*piece,order['filled'],order['side'])

    def add_trade(self,price,quantity,side):#Создание сделки
        trade = {'id': self.trade_id, 'price': price, 'quantity': quantity, 'side': side, 'timestamp': '2018-06-10T08:14:47.675Z'}
        self.trade_id += 1
        self.trades.append(trade)

