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
            self.balances = self.db.balances
            status = 'OK'
        except Exception as e:
            status = 'ERROR: ' + str(e)
        print('MongoDB status... ' + status)

    def get_entries(self, collection_name=None, _filter={}):
        if bool(collection_name) and hasattr(self, collection_name):
            return [i for i in getattr(self, collection_name).find(_filter)]

    def add_entry(self, collection_name=None, data=None):
        if bool(collection_name) and hasattr(self, collection_name) and isinstance(data, dict):
            getattr(self, collection_name).insert_one(data)

    def update_entry(self, collection_name=None, _filter=None, data=None):
        if bool(collection_name) and hasattr(self, collection_name) and isinstance(_filter, dict) and isinstance(data, dict):
            getattr(self, collection_name).update_one(_filter, {'$set': data}, upsert=False)
