#!/usr/bin/python
# -*- coding: utf-8 -*-
from config import *
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
            status = 'OK'
        except Exception as e:
            status = 'ERROR: ' + str(e)
        print('MongoDB status... ' + status)

    def get_entries(self, collection_name=None):
        if bool(collection_name) and hasattr(self, collection_name):
            return [i for i in getattr(self, collection_name).find()]

    def add_entry(self, collection_name=None, data=None):
        if bool(collection_name) and hasattr(self, collection_name) and isinstance(data, dict):
            getattr(self, collection_name).insert_one(data)
