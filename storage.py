#!/usr/bin/python
# -*- coding: utf-8 -*-

from config import *
from pymongo import MongoClient


class BotDataStorage:
    def __init__(self):
        try:
            self.client = MongoClient('{}:{}'.format(DEFAULT_HOST, MONGODB_PORT))
            self.db = self.client[MONGO_DB_NAME]
            self.orders = self.db.orders
            self.history = self.db.history
            status = 'OK'
        except Exception as e:
            status = 'ERROR: ' + str(e)
        print('MongoDB status... ' + status)

    def store_order(self, data):
        if self.orders and isinstance(data, dict):
            self.orders.insert_one(data)

    def add_history_point(self, data):
        if self.history and isinstance(data, dict):
            self.history.insert_one(data)


class StockDataStorage:
    pass
