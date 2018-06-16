#!/usr/bin/python
# -*- coding: utf-8 -*-

from config import *
import subprocess
from bottle import run, request, route


@route('/<path>', method='POST')
def process(path):
    incoming = request.POST.dict
    print(incoming)
    # return subprocess.check_output(['python3', path+'.py'],shell=True)


run(host=DEFAULT_HOST, port=API_PORT, debug=False)

