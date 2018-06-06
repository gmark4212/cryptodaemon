#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from config import *
import storage, telegram
from strategy import Strategy
from time import sleep


class CryptoBot:
    def __init__(self, trading_strategy=None, emulation_mode=False):
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
                        self.base_balance = balance['available']
                        break
            else:
                return currencies_balances

    def fetch_prices(self, pair):
        if self.strategy:
            data = self.strategy.exchange.fetch_ticker(pair)
            return data['last']
        return 0

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
                tickers_quantity = len(s.suitable_tickers)
                if tickers_quantity > 0:
                    self.fetch_balance()
                    if self.base_balance > 0:
                        whole_money_to_spend = self.get_summ_to_spend_to_buy()
                        if whole_money_to_spend > 0:
                            self.money_per_buy_order = whole_money_to_spend/tickers_quantity
                            for symbol in s.suitable_tickers:
                                price = self.fetch_prices('{}/{}'.format(symbol, BASE_TICKER))
                                if price > 0:
                                    stop_price = price + (price * (s.your_margin_pct/100))
                                    amount = self.money_per_buy_order/price
                                    self.place_order(symbol, amount, price, BUY)
                                    # todo: check order state. sell when executed
                                    self.place_order(symbol, amount, stop_price, SELL)

    def stop_trading(self):
        self.keep_working = False


if __name__ == '__main__':
    bot = CryptoBot(Strategy(), '-e' in sys.argv)
    bot.start_trading()
