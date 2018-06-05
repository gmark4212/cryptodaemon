#!/usr/bin/python
# -*- coding: utf-8 -*-

from config import *
import argparse
import storage, telegram
from strategy import Strategy
from time import sleep


class CryptoBot:
    def __init__(self, trading_strategy=None):
        self.base_balance = None
        self.money_per_buy_order = 0
        self.keep_working = True
        if isinstance(trading_strategy, Strategy):
            self.strategy = trading_strategy

    def fetch_balance(self, base_currency_only=True):
        if self.strategy:
            data = self.strategy.exchange.fetch_balance()
            currencies_balances = data['info']
            if base_currency_only:
                for balance in currencies_balances:
                    if balance['currency'] == BASE_TICKER:
                        self.base_balance = balance
                        break
            else:
                return currencies_balances

    def get_summ_to_spend_to_buy(self):
        if self.strategy and self.base_balance>0:
            return self.base_balance * ((100-self.strategy.deposit_threshold_pct)/100)
        return 0

    def place_order(self, symbol, amount, price, side=None):
        if bool(side) and bool(symbol) and amount > 0 and price > 0:
            self.strategy.exchange.create_order(symbol, 'limit', side, amount, price)

    def start_trading(self):
        self.keep_working = True
        s = self.strategy
        if s.type == ROLLBACK:
            while self.keep_working:
                sleep(INTERVAL)
                s.fetch_suitable_coins()
                self.fetch_balance()
                whole_money_to_spend = self.get_summ_to_spend_to_buy()
                tickers_quantity = len(s.suitable_tickers)
                if whole_money_to_spend > 0 and tickers_quantity > 0:
                    self.money_per_buy_order = whole_money_to_spend/tickers_quantity
                    for symbol in s.suitable_tickers:
                        # todo: place buy order, than sell with stop-price = price + your margin pct + exchange fee
                        pass

    def stop_trading(self):
        self.keep_working = False


if __name__ == '__main__':

    bot = CryptoBot(Strategy())
    bot.start_trading()
