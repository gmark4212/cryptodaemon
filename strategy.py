#!/usr/bin/python
# -*- coding: utf-8 -*-
from config import *
from coinmarketcap import Market


class Strategy:
    def __init__(self, exchange=None, **kwargs):
        self.exchange = exchange if exchange else DEFAULT_EXCHANGE
        self.type = 'scalping'
        self.purchase_different_coins = 3  # 3-10 recommended
        self.drop_range_to_buy_pct = range(-40, -10)
        self.deposit_threshold_pct = 50
        self.capitalization_threshold_usd = float(50000000.0)  # > 30 billions recommended
        self.market_volume_threshold_usd_24h = 500000
        self.your_margin_pct = 10
        self.market = Market()
        self.drops = None
        self.suitable_coins_marketcap = {}
        self.coins_listing = {item['symbol']: {'id': item['id'], 'name': item['name']} for item in self.market.listings()['data']}
        for key in kwargs:
            if hasattr(self, key):
                self[key] = kwargs[key]

    def fetch_suitable_coins(self):
        tickers = self.exchange.fetch_tickers()
        self.drops = {pair: data for pair, data in tickers.items()
                      if pair.endswith(BASE_TICKER) and int(data['percentage']) in self.drop_range_to_buy_pct}

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
                                    self.suitable_coins_marketcap[ticker] = market_data
                else:
                    print('Не могу узнать капитализацию: {}, пропускаю'.format(ticker))


# if __name__ == '__main__':
#
#     s = Strategy()
#     print(s.capitalization_threshold_usd )
#     s.fetch_suitable_coins()
