#!/usr/bin/python
# -*- coding: utf-8 -*-


class Strategy:
    def __init__(self):
        self.type = 'scalping'
        self.purchase_different_coins = 3
        self.drop_range_to_buy_pct = [10, 40]
        self.deposit_threshold_pct = 50
        self.capitalization_threshold_usd = 20000000000
        self.market_volume_threshold_usd_24h = 500000
        self.your_margin_pct = 10