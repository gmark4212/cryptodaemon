#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from config import *
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
import json
from strategy import Strategy
from cryptobot import CryptoBot
from multiprocessing import Process


class ProcessManager:
    def __init__(self):
        self.workers = {}

    def add_worker(self, data):
        if self.request_is_valid(data) and self.find_worker(data['id']) is None:
            ss = 'strategy-settings'
            strategy_settings = data[ss] if ss in data else {}
            cb = CryptoBot(Strategy(None, **strategy_settings), True)
            stream = Process(target=cb.start_trading)
            try:
                # stream.daemon = True
                stream.start()
                self.workers[data['id']] = stream
                return True
            except Exception as e:
                print(e)
                return False

    @staticmethod
    def request_is_valid(d):
        basic = 'action' in d and 'id' in d
        return basic

    def find_worker(self, uid):
        if uid in self.workers:
            return self.workers[uid]

    def kill_worker(self, uid):
        # todo: not stop!
        worker = self.find_worker(uid)
        if worker:
            try:
                worker.terminate()
                self.workers.remove(worker)
                print(worker, ' killed')
            except:
                return False
            else:
                return True


class PostHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.pm = ProcessManager()
        super(PostHandler, self).__init__(*args, **kwargs)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        data = json.loads(body.decode(ENCODING))
        self.process_query(data)

    def process_query(self, data):
        if 'action' in data:
            uid = data['id']
            # todo: set exchange by name + api key
            if data['action'] == 'start':
                started = self.pm.add_worker(data)
                print(self.pm.workers)
                if started is None:
                    self.respond(WRONG_DATA, 'CryptoDaemon already started')
                elif started:
                    self.respond(SUCCESS, 'CryptoDaemon started successfully')
                else:
                    self.respond(SERVER_ERROR, 'Shit happened. ')
            elif data['action'] == 'stop':
                if self.pm.kill_worker(uid):
                    self.respond(SUCCESS, 'CryptoDaemon instance stopped')
                else:
                    self.respond(SERVER_ERROR, 'Your bot is unstoppable!')
            else:
                self.respond(WRONG_DATA, 'Unknown action!')

    def respond(self, code, answer):
        self.send_response(code)
        self.end_headers()
        response = BytesIO()
        response.write(bytes(answer, ENCODING))
        self.wfile.write(response.getvalue())


if __name__ == '__main__':
    httpd = HTTPServer((DEFAULT_HOST, API_PORT), PostHandler)
    httpd.serve_forever()



