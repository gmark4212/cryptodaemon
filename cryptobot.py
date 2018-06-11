#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
from config import *
from strategy import Strategy
from time import sleep
from emulator import MockExchange
from storage import BotDataStorage


class CryptoBot:
    def __init__(self, trading_strategy, emulation_mode=False):
        self.base_balance = None
        self.money_per_buy_order = 0
        self.keep_working = True
        self._buy_orders = []
        self.db = BotDataStorage()
        if isinstance(trading_strategy, Strategy):
            self.strategy = trading_strategy
            self.exchange = MockExchange() if emulation_mode else self.strategy.exchange
        else:
            raise TypeError

    def fetch_balance(self, base_currency_only=True):
        data = self.exchange.fetch_balance()
        currencies_balances = data['info']
        if base_currency_only:
            for balance in currencies_balances:
                if balance['currency'] == BASE_TICKER:
                    self.base_balance = float(balance['available'])
                    break
        else:
            return currencies_balances

    def fetch_prices(self, pair):
        return float(self.exchange.fetch_ticker(pair)['last'])

    def fetch_my_open_orders(self, pair=None):
        return self.exchange.fetch_open_orders(self, symbol=pair)

    def get_summ_to_spend_to_buy(self):
        if self.base_balance > 0:
            return self.base_balance * ((100-self.strategy.deposit_threshold_pct)/100)
        return 0

    def get_order_state(self, oid): #???? в oid попадает весь ордер а не его номер ????
        if oid:
            oid = oid['id']
            return self.exchange.fetch_order(self, id=oid)['status']

    def place_order(self, symbol, amount, price, side=None):
        order = None
        if bool(side) and bool(symbol) and amount > 0 and price > 0:
            typer = 'stopLimit' if side == SELL else 'limit'
            try:
                order = self.exchange.create_order(symbol, typer, side, amount, price)
                if order['side'] == BUY:
                    self.db.store_order(order)
            except Exception as e:
                print(e)
                pass
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
        s = self.strategy
        print('Starting trade...')
        if s.type == ROLLBACK:
            while self.keep_working:
                s.fetch_suitable_coins()
                tickers_quantity = len(s.suitable_tickers)
                print('SUITABLE COINS: ', s.suitable_tickers)
                if tickers_quantity > 0:
                    self.fetch_balance()
                    print('ACCOUNT BALANCE: ', self.base_balance)
                    if self.base_balance > 0:
                        whole_money_to_spend = self.get_summ_to_spend_to_buy()
                        print('MONEY TO SPEND: ', whole_money_to_spend)
                        if whole_money_to_spend > 0:
                            self.money_per_buy_order = whole_money_to_spend/tickers_quantity
                            print('MONEY FOR 1 ORDER: ', self.money_per_buy_order)
                            for symbol in s.suitable_tickers:
                                price = self.fetch_prices('{}/{}'.format(symbol, BASE_TICKER))
                                print('LAST PRICE FOR {}: {} '.format(symbol, price))
                                if price > 0:
                                    amount = round(self.money_per_buy_order/price, -3)
                                    print('AMOUNT TO BUY {}: {} '.format(symbol, amount))
                                    self._buy_orders.append(self.place_order(symbol, amount, price, BUY))
                else:
                    print('No suitable coins for this strategy at a moment')

                for buy_order in self._buy_orders:
                    if self.get_order_state(buy_order) == 'filled':
                        # check order state. sell when executed
                        price = buy_order['price']
                        stop_price = price + (price * (s.your_margin_pct / 100))
                        sell_order = self.place_order(buy_order['symbol'], buy_order['quantity'], stop_price, SELL)
                        if sell_order:
                            self.db.store_order(sell_order)
                            self._buy_orders.remove(buy_order)
                sleep(INTERVAL)

    def stop_trading(self):
        self.keep_working = False


if __name__ == '__main__':
    # bot = CryptoBot(Strategy(), '-e' in sys.argv )
    bot = CryptoBot(Strategy(), True) # '-e' in sys.argv выдает False
    bot.start_trading()



