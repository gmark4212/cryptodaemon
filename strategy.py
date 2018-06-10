#!/usr/bin/python
# -*- coding: utf-8 -*-
from config import *
from coinmarketcap import Market


class Strategy:
    def __init__(self, exchange=None, **kwargs):
        print('Strategy initializing...')
        self.exchange = exchange if exchange else DEFAULT_EXCHANGE
        self.type = ROLLBACK
        self.purchase_different_coins = 3  # 3-10 recommended
        self.drop_range_to_buy_pct = range(-40, -10)
        self.deposit_threshold_pct = 50
        self.capitalization_threshold_usd = float(20000000.0)  # > 30 billions recommended
        self.market_volume_threshold_usd_24h = 500000
        self.your_margin_pct = 10
        self.market = Market()
        self.drops = None
        self.suitable_coins_marketcap = {}
        self.suitable_tickers = []
        self.coins_listing = {item['symbol']: {'id': item['id'], 'name': item['name']} for item in self.market.listings()['data']}
        self.crypto_only = False  # include tokens, ico etc.
        self.currencies = None
        for key in kwargs:
            if hasattr(self, key):
                self[key] = kwargs[key]

    def fetch_currencies(self):
        curs = self.exchange.fetch_currencies()
        if self.crypto_only:
            curs = dict((k + '/' + BASE_TICKER, v) for k, v in curs.items() if v['type'] == 'crypto')
        else:
            curs = dict((k + '/' + BASE_TICKER, v) for k, v in curs.items())
        self.currencies = curs

    def fetch_suitable_coins(self):
        self.fetch_currencies()
        tickers = self.exchange.fetch_tickers()
        self.drops = {pair: data for pair, data in tickers.items()
                      if pair.endswith(BASE_TICKER)
                      and data['percentage'] is not None
                      and int(data['percentage']) in self.drop_range_to_buy_pct
                      and pair in self.currencies}
        if self.market:
            for pair, market_data in self.drops.items():
                ticker = pair.split('/')[0]
                if ticker in self.coins_listing:
                    market_cap_id = self.coins_listing[ticker]['id']
                    if bool(market_cap_id):
                        market_data = self.market.ticker(market_cap_id, convert=USD)['data']['quotes'][USD]
                        capital = market_data['market_cap']
                        if isinstance(capital, float):
                            if capital >= self.capitalization_threshold_usd:
                                    print(ticker, capital)
                                    self.suitable_coins_marketcap[ticker] = capital
                else:
                    print('Capitalization is unknown: {}... pass'.format(ticker))
                if len(self.suitable_coins_marketcap) > 0:
                    scm = self.suitable_coins_marketcap
                    self.suitable_tickers = sorted(scm, key=scm.get, reverse=True)[:self.purchase_different_coins]


if __name__ == '__main__':

    s = Strategy()
    s.fetch_suitable_coins()
    print(s.suitable_tickers)
