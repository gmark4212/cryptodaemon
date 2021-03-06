#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from config import *
from lib import *
from strategy import Strategy
from time import sleep
from mock import FakeExchange
from storage import BotDataStorage


class CryptoBot:
    def __init__(self, trading_strategy, emulation_mode=False, uid=None):
        self.money_per_buy_order = 0
        self.keep_working = True
        self._buy_orders = []
        self._sell_orders = []
        self.uid = uid
        self.emulated = emulation_mode
        if isinstance(trading_strategy, Strategy):
            self.strategy = trading_strategy
            if emulation_mode:
                self.exchange = FakeExchange()
                self.exchange.strategy = self.strategy
            else:
                self.exchange = self.strategy.exchange
        else:
            raise TypeError
        self.base_balance = self.fetch_balance()

    def fetch_balance(self, base_currency_only=True):
        data = self.exchange.fetch_balance()
        if self.emulated:
            return data
        currencies_balances = data['info']
        if base_currency_only:
            for balance in currencies_balances:
                if balance['currency'] == BASE_TICKER:
                    balance[LIMIT] = self.get_limit_deposit(float(balance[AVAILABLE]))
                    return balance
        else:
            return currencies_balances

    def fetch_prices(self, pair):
        return float(self.exchange.fetch_ticker(pair)['last'])

    def fetch_my_open_orders(self, pair=None):
        return self.exchange.fetch_open_orders(self, symbol=pair)

    def get_summ_to_spend_to_buy(self):
        return max(float(self.base_balance[AVAILABLE]) - float(self.base_balance[LIMIT]), 0)

    def get_limit_deposit(self, available_money):
        return max(available_money * (self.strategy.deposit_threshold_pct / 100), 0)

    def get_funds_stop_limit(self):
        return self.get_limit_deposit(float(self.base_balance[AVAILABLE]))

    def get_order_state(self, order):
        if isinstance(order, dict):
            if order.get('id') is not None:
                return self.exchange.fetch_order(oid=order['id'])['status']

    def place_order(self, symbol, amount, price, side=None):
        order = None
        if bool(side) and bool(symbol) and amount > 0 and price > 0:
            typer = STOP_LIMIT if side == SELL else LIMIT
            params = dict(stopPrice=price) if side == SELL else {}
            order = self.exchange.create_order(symbol, typer, side, amount, price, params)
            wprint(self.uid, '+ NEW ORDER: ', order['side'], order['symbol'], order['price'],
                  order['amount'], order['id'], order['datetime'])
            if self.emulated and side == BUY and isinstance(order, dict):
                self.exchange.buy_new_money_shift(amount * price)
        return order

    def calculate_profit(self, since):
        balance = {SELL: 0, BUY: 0}
        trades = self.exchange.fetch_my_trades(since=since)
        for i in trades:
            side = i['side']
            trade_summ = float(i['price']) + float(i['fee']) if side == BUY else float(i['price']) - float(i['fee'])
            balance[side] += trade_summ
        return balance[SELL] - balance[BUY]

    def start_trading(self):
        self.keep_working = True
        self.base_balance[LIMIT] = self.get_funds_stop_limit()
        s = self.strategy
        # db initialises here due problem to writing mongo from fork
        db = BotDataStorage()
        wprint(self.uid, 'Starting trade...')

        if s.type == ROLLBACK:
            while self.keep_working:
                self.base_balance = self.fetch_balance()
                wprint(self.uid, 'ACCOUNT BALANCE: ', self.base_balance)

                db.replace_entry(BALANCES, dict(uid=self.uid), dict(uid=self.uid, balance=self.base_balance))

                if float(self.base_balance[AVAILABLE]) > self.base_balance[LIMIT]:
                    s.fetch_suitable_coins()
                    tickers_quantity = len(s.suitable_tickers)
                    wprint(self.uid, 'SUITABLE COINS: ', s.suitable_tickers)
                    if tickers_quantity > 0:
                        whole_money_to_spend = self.get_summ_to_spend_to_buy()
                        wprint(self.uid, 'MONEY TO SPEND: ', whole_money_to_spend)
                        if whole_money_to_spend > 0:
                            self.money_per_buy_order = whole_money_to_spend/tickers_quantity
                            wprint(self.uid, 'MONEY FOR 1 ORDER: ', self.money_per_buy_order)
                            for ticker in s.suitable_tickers:
                                symbol = '{}/{}'.format(ticker, BASE_TICKER)
                                price = self.fetch_prices(symbol)
                                wprint(self.uid, 'LAST PRICE FOR {}: {} '.format(symbol, price))
                                if price > 0:
                                    amount = self.money_per_buy_order/price
                                    if amount > 0:
                                        wprint(self.uid, 'AMOUNT TO BUY {}: {} '.format(symbol, amount))
                                        self._buy_orders.append(self.place_order(symbol, amount, price, BUY))
                    else:
                        wprint(self.uid, 'No suitable coins for this strategy at the moment')
                # else:
                #     print('You are out of funds ', self.base_balance)

                sleep(INTERVAL)
                for buy_order in self._buy_orders:
                    if self.get_order_state(buy_order) == EXECUTED:
                        # check order state. sell when executed
                        price = float(buy_order['price'])
                        stop_price = price + (price * (s.your_margin_pct / 100))
                        buy_amount = float(buy_order['amount'])
                        sell_order = self.place_order(buy_order['symbol'], buy_amount, stop_price, SELL)
                        self._sell_orders.append(sell_order)
                        if self.emulated:
                            self.exchange.buy_executed_money_shift(price * buy_amount)
                        self.store_history(buy_order, db)
                        self._buy_orders.remove(buy_order)

                sleep(INTERVAL)
                for sell_order in self._sell_orders:
                    if self.get_order_state(sell_order) == EXECUTED:
                        if self.emulated:
                            self.exchange.sell_executed_money_shift(float(sell_order['price']) * float(sell_order['amount']))
                        self.store_history(sell_order, db)
                        self._sell_orders.remove(sell_order)

    def store_history(self, order, db=None):
        if db:
            db.add_entry(HISTORY, dict(uid=self.uid, utc=utc_now(), balance=self.exchange.fetch_balance(), order=order))

    def stop_trading(self):
        self.keep_working = False
        self.__del__()

    def __del__(self):
        wprint(self.uid, 'Daemon killed...')


if __name__ == '__main__':
    # bot = CryptoBot(Strategy(), '-e' in sys.argv)
    bot = CryptoBot(Strategy(), True)
    bot.start_trading()
