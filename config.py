#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from ccxt import hitbtc2

# general
APP_NAME = 'CryptoDaemonBot'
APP_VERSION = '0.2'
INTERVAL = 30

# dirs
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# keys
API_KEYS = {'hitbtc': dict(api='aeac732a33236d840e4beccfced63754', secret='17e70f8a123e2b90fd0440c0deb6f3a6')}

# exchanges
DEFAULT_EXCHANGE = hitbtc2({
    "apiKey": API_KEYS['hitbtc']['api'],
    "secret": API_KEYS['hitbtc']['secret'],
    "enableRateLimit": True,
})

# currency
BASE_TICKER = 'BTC'
USD = 'USD'

# strategies
ROLLBACK = 'rollback'

# sides
SELL = 'sell'
BUY = 'buy'


