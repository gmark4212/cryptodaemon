#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from ccxt import hitbtc2

# general
APP_NAME = 'CryptoDaemonBot'
APP_VERSION = '0.3'
INTERVAL = 6
DEFAULT_HOST = 'localhost'
API_PORT = 8888
ENCODING = 'utf-8'

# emulation
FAKE_DEPOSIT = 2

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

DEFAULT_EXCH_CLASS = DEFAULT_EXCHANGE.__class__

# profit policies
FULL_REINVEST = 'full-reinvest'
HALF_REINVEST = 'half-reinvest'
FULL_TAKE = 'full-take'

# currency
BASE_TICKER = 'BTC'
USD = 'USD'

# strategies
ROLLBACK = 'rollback'

# sides
SELL = 'sell'
BUY = 'buy'

# order statuses
NEW = 'new'
SUSPENDED = 'suspended'
PARTIAL = 'partiallyFilled'
EXECUTED = 'filled'
CANCELED = 'canceled'
EXPIRED = 'expired'

# order types
LIMIT = 'limit'
MARKET = 'market'
STOP_LIMIT = 'stopLimit'
STOP_MARKET = 'stopMarket'

# balance
AVAILABLE = 'available'
RESERVED = 'reserved'
LIMIT = 'limit'

# emulation
# FAKE_BALANCE = 1

# database
MONGODB_PORT = 27017
MONGO_DB_NAME = 'cryptodaemon'
STORE_HISTORY = True

# telegram
TOKEN = '602258813:AAHBxMU8FfXHRo4mD3ZyyLobgHdvO8yUWtU'
COMMANDS = {
            'help': 'Предоставляет информацию о доступных командах',
            'run': 'Запускает CryptoBot',
            'stop': 'Останавливает CryptoBot',
            'balance': 'Предоставляет информацию о текущем балансе'
}