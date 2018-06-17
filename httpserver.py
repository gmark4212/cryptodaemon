#!/usr/bin/python
# -*- coding: utf-8 -*-
from config import *
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
import json
from strategy import Strategy
from cryptobot import CryptoBot
from multiprocessing import Process


class PostHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        data = json.loads(body.decode(ENCODING))
        self.process_query(data)

    def process_query(self, data):
        if 'request-type' in data:
            if data['request-type'] == 'cryptobot-start':
                strategy_settings = data['strategy-settings']
                cb = CryptoBot(Strategy(None, **strategy_settings), True)
                p = Process(target=cb.start_trading)
                p.start()
                self.respond('OK')

    def respond(self, answer):
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(bytes(answer, ENCODING))
        self.wfile.write(response.getvalue())


if __name__ == '__main__':
    httpd = HTTPServer((DEFAULT_HOST, API_PORT), PostHandler)
    httpd.serve_forever()