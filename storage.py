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
            self.logs = self.db.logs
            self.workers = self.db.workers
            status = 'OK'
        except Exception as e:
            status = 'ERROR: ' + str(e)
        print('MongoDB status... ' + status)

    def get_entries(self, collection_name=None):
        if bool(collection_name) and hasattr(self, collection_name):
            return [i for i in self[collection_name].find()]

    def add_entry(self, collection_name=None, data=None):
        if bool(collection_name) and hasattr(self, collection_name) and isinstance(data, dict):
            getattr(self, collection_name).insert_one(data)


class Log:
    def __init__(self, db=None):
        self.db = db

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
                mes = {'time': ctime(), 'INFO': info, 'module_name': decorated.__name__, 'module': decorated.__module__}
                self.db.add_log_info(mes)
                return result
            return decorated
        return func
