#!/usr/bin/python
# -*- coding: utf-8 -*-

from config import *
import argparse
import storage, telegram
from strategy import Strategy


class CryptoBot:
    def __init__(self, trading_strategy=None):
        self.base_balance = None
        if isinstance(trading_strategy, Strategy):
            self.strategy = trading_strategy

    def fetch_balance(self, base_currency_only=True):
        if self.strategy:
            ex = self.strategy.exchange
            data = ex.fetch_balance()
            currencies_balances = data['info']
            if base_currency_only:
                for balance in currencies_balances:
                    if balance['currency'] == BASE_TICKER:
                        self.base_balance = balance
            else:
                return currencies_balances

    def start_trading(self):
        pass

    def stop_trading(self):
        pass


if __name__ == '__main__':

    bot = CryptoBot(Strategy())
    bot.start_trading()
