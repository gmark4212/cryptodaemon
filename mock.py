#!/usr/bin/python
# -*- coding: utf-8 -*-
from config import *
from lib import *


class FakeExchange(DEFAULT_EXCH_CLASS):
    def __init__(self):
        self.balance = dict(currency=BASE_TICKER, available=FAKE_DEPOSIT, reserved=0)
        self.orders = {}
        self.strategy = None

    @staticmethod
    def _correct_order_status_by_true_market(order):
        params = {'sort': 'ASC', 'by': 'timestamp','from': order['timestamp']}
        try:
            public_trades = DEFAULT_EXCHANGE.fetch_trades('{}/{}'.format(order['symbol'], BASE_TICKER), limit=None, params=params)
            for i in public_trades:
                if i['side'] == order['side']:
                    print(order['symbol'],order['datetime'], order['price'], i['price'])
                    if i['price'] >= order['price']:
                        order['status'] = EXECUTED
                        break
        except Exception as e:
            print(e)
        return order

    def buy_new_money_shift(self, summ):
        self.balance[AVAILABLE] -= summ
        self.balance[RESERVED] += summ

    def buy_executed_money_shift(self, summ):
        self.balance[RESERVED] -= summ

    def sell_executed_money_shift(self, summ):
        if self.strategy == FULL_TAKE:
            self.balance[AVAILABLE] += summ
            self.balance[LIMIT] += summ
        elif self.strategy == HALF_REINVEST:
            self.balance[AVAILABLE] += summ
            self.balance[LIMIT] += summ/2
        elif self.strategy == FULL_REINVEST:
            self.balance[AVAILABLE] += summ
        print('+ GET PROFIT: ', summ)

    def fetch_balance(self):
        return self.balance

    def fetch_order(self, oid):
        order = self.orders[oid]
        if isinstance(order, dict):
            return self._correct_order_status_by_true_market(order)

    def create_order(self, symbol, typer, side, amount, price=None, params={}):
        now = utc_now()
        uuid = self.uuid()
        parts = uuid.split('-')
        clientOrderId = ''.join(parts)
        clientOrderId = clientOrderId[0:32]
        amount = float(amount)
        response = {
            'clientOrderId': clientOrderId,
            'quantity': amount,
            'id': clientOrderId,
            'timestamp': now,
            'createdAt': now,
            'datetime':  None,
            'lastTradeTimestamp': None,
            'status': NEW,
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
        order = self.parse_order(response)
        id = order['id']
        self.orders[id] = order
        return order

    def parse_order(self, order, market=None):
        created = None
        if 'createdAt' in order:
            created = self.parse8601(order['createdAt'])
        updated = None
        if 'updatedAt' in order:
            updated = self.parse8601(order['updatedAt'])
        symbol = order['symbol']
        amount = self.safe_float(order, 'quantity')
        filled = self.safe_float(order, 'cumQuantity')
        status = order['status']
        if status == 'new':
            status = 'open'
        elif status == 'suspended':
            status = 'open'
        elif status == 'partiallyFilled':
            status = 'open'
        elif status == 'filled':
            status = 'closed'
        id = str(order['clientOrderId'])
        price = self.safe_float(order, 'price')
        if price is None:
            if id in self.orders:
                price = self.orders[id]['price']
        remaining = None
        cost = None
        if amount is not None:
            if filled is not None:
                remaining = amount - filled
                if price is not None:
                    cost = filled * price
        return {
            'id': id,
            'timestamp': created,
            'datetime': self.iso8601(created),
            'lastTradeTimestamp': updated,
            'status': status,
            'symbol': symbol,
            'type': order['type'],
            'side': order['side'],
            'price': price,
            'amount': amount,
            'cost': cost,
            'filled': filled,
            'remaining': remaining,
            'fee': None,
            'info': order,
        } 

    @staticmethod
    def fetch_ticker(pair):
        return DEFAULT_EXCHANGE.fetch_ticker(pair)

    def fetch_my_trades(self, since):
        pass

