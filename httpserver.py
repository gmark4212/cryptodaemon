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
            cb = CryptoBot(Strategy(data['exchange'], **strategy_settings), True)
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
        try:
            self.workers[uid].terminate()
            self.workers.remove(self.workers[uid])
            print(' killed!')
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

    @staticmethod
    def keys_structured(api_key, secret_key):
        return dict(apiKey=api_key, secret=secret_key, enableRateLimit=True)

    def process_query(self, data):
        print(data)
        if 'action' in data:
            # set exchange by name + api key
            if data['action'] == 'start':
                if 'exchange' in data and 'public_key' in data and 'secret_key' in data:
                    ex = SUPPORTED_EXCHANGES[data['exchange']]
                    if ex is None:
                        self.respond(WRONG_DATA, 'Non supported exchange!')
                        return False
                    else:
                        data['exchange'] = ex(self.keys_structured(data['public_key'], data['secret_key']))
                else:
                    self.respond(WRONG_DATA, 'Exchange or API-key unfilled!')
                    return False

                started = self.pm.add_worker(data)
                print(self.pm.workers)
                if started is None:
                    self.respond(WRONG_DATA, 'CryptoDaemon already started')
                elif started:
                    self.respond(SUCCESS, 'CryptoDaemon started successfully')
                else:
                    self.respond(SERVER_ERROR, 'Shit happened. ')
            elif data['action'] == 'stop':
                if self.pm.kill_worker(data['id']):
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
