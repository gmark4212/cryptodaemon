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
            status = 'OK'
        except Exception as e:
            status = 'ERROR: ' + str(e)
        print('MongoDB status... ' + status)

    def add_history_point(self, data):
        if self.history and isinstance(data, dict):
            self.history.insert_one(data)

    def add_log_info(self, info):
        if self.logs and isinstance(info, dict):
            self.logs.insert_one(info)

    def get_logs(self):
        if self.db.logs:
            logs = []
            for log in self.db.logs.find():
                logs.append(log)
            return logs


class Log:
    def __init__(self, db=None):
        self.db = db

    @staticmethod
    def _create_message(result=None, *args, **kwargs):
        info = ''
        if args:
            info += 'args: {} '.format(args)
        if kwargs:
            info += 'kwargs: {} '.format(kwargs)
        if result:
            info += '= {}'.format(result)
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
