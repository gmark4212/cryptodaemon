#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from ccxt import hitbtc2, poloniex, exmo

# general
APP_NAME = 'CryptoDaemonBot'
APP_VERSION = '0.5'
INTERVAL = 6
DEFAULT_HOST = '127.0.0.1'
API_PORT = 8888
ENCODING = 'utf-8'

# stat consumer api
# STAT_CONSUMER = 'http://{}:8000/bot_api/stat/'.format(DEFAULT_HOST)
STAT_CONSUMER = 'https://cryptodaemon.cloud/bot_api/stat/'

# emulation
FAKE_DEPOSIT = 2

# dirs
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# keys
API_KEYS = {'hitbtc': dict(api='aeac732a33236d840e4beccfced63754', secret='17e70f8a123e2b90fd0440c0deb6f3a6')}

# exchanges
SUPPORTED_EXCHANGES = dict(hitbtc=hitbtc2, poloniex=poloniex, exmo=exmo)
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
OPEN = 'open'

# order types
LIMIT = 'limit'
MARKET = 'market'
STOP_LIMIT = 'stopLimit'
STOP_MARKET = 'stopMarket'

# balance
AVAILABLE = 'available'
RESERVED = 'reserved'
LIMIT = 'limit'

# database
MONGODB_PORT = 27017
MONGO_DB_NAME = 'cryptodaemon'
STORE_HISTORY = True

# collections
HISTORY = 'history'
ORDERS = 'orders'
BALANCES = 'balances'

# telegram
TOKEN = '602258813:AAHBxMU8FfXHRo4mD3ZyyLobgHdvO8yUWtU'
COMMANDS = {
            'help': 'Предоставляет информацию о доступных командах',
            'run': 'Запускает CryptoBot',
            'stop': 'Останавливает CryptoBot',
            'balance': 'Предоставляет информацию о текущем балансе'
}

# API codes
SUCCESS = 200
SERVER_ERROR = 500
WRONG_DATA = 400
NOT_IMPLEMENTED = 501

# request keys
AKEY = 'api_keys'
ACTION = 'action'
PKEY = 'public_key'
SKEY = 'secret_key'
EXCHANGE = 'exchange'