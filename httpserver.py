#!/usr/bin/python
# -*- coding: utf-8 -*-
from config import *
from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
import json


class POSTRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        data = json.loads(body.decode(ENCODING))
        print(data)

    def respond(self, answer):
        self.send_response(200)
        self.end_headers()
        response = BytesIO()
        response.write(bytes(answer, ENCODING))
        self.wfile.write(response.getvalue())


if __name__ == '__main__':
    httpd = HTTPServer((DEFAULT_HOST, API_PORT), POSTRequestHandler)
    httpd.serve_forever()