#!/usr/bin/python
# -*- coding: utf-8 -*-

from config import *
from lib import *
from pymongo import MongoClient

from functools import wraps

from time import ctime


class BotDataStorage:
    def __init__(self):
        try:
            self.client = MongoClient('{}:{}'.format(DEFAULT_HOST, MONGODB_PORT))
            self.db = self.client[MONGO_DB_NAME]
            self.orders = self.db.orders
            self.history = self.db.history
            self.logs = self.db.logs
            self.trades = self.db.trades
            status = 'OK'
        except Exception as e:
            status = 'ERROR: ' + str(e)
        print('MongoDB status... ' + status)

    def add_history_point(self, data):
        if isinstance(data, dict):
            self.history.insert_one(data)

    def get_stories(self):
        stories = []
        for story in self.history.find():
            stories.append(story)
        return stories

    def add_order(self, order):
        if isinstance(order, dict):
            # order['time'] = ctime()
            # if order['status'] == EXECUDET:
            #     order['datetime'] = utc_now()
            self.orders.insert_one(order)

    def get_orders(self, symbol=None, status=None, side=None):
        params = {}
        if symbol:
            params['symbol'] = symbol
        if status:
            params['status'] = status
        if side:
            params['side'] = side
        orders = []
        for order in self.orders.find(params):
            orders.append(order)
        return orders

    def add_log_info(self, info):
        if isinstance(info, dict):
            self.logs.insert_one(info)

    def get_logs(self):
        logs = []
        for log in self.db.logs.find():
            logs.append(log)
        return logs

    def add_trade(self, trade):
        if isinstance(trade, dict):
            self.trades.insert_one(trade)

    def get_trades(self):
        trades = []
        for trade in self.db.trades.find():
            trades.append(trade)
        return trades

    def get_full_statistic(self):
        stories = self.get_stories()
        open_orders = self.get_orders(status=OPEN)
        closed_orders = self.get_orders(status=EXECUDET)
        logs = self.get_logs()
        trades = self.get_trades()
        statistic = {
            'work_info': logs,
            'open_orders': open_orders,
            'closed_orders': closed_orders,
            'trades': trades,
            'stories': stories
        }
        return statistic

    def drop_collection(self, collection_name):
        self.db[collection_name].drop()

    def drop_database(self):
        self.orders.drop()
        self.history.drop()
        self.logs.drop()
        self.trades.drop()




class Log:
    def __init__(self):
        self.db = BotDataStorage() if STORE_HISTORY else None

    @staticmethod
    def _create_message(result=None, *args, **kwargs):
        info = {}
        if args:
            info['args'] = args
        if kwargs:
            info['kwargs'] = kwargs
        if result:
            info['result'] = result
        return info

    def __call__(self, func):
        if self.db:
            @wraps(func)
            def decorated(*args, **kwargs):
                result = func(*args, **kwargs)
                info = Log._create_message(result, *args, **kwargs)
                mes = {'time': ctime(), 'INFO': info, 'module_name': decorated.__name__}
                self.db.add_log_info(mes)
                return result
            return decorated
        return func


logger = Log()
