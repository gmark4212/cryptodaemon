#!/usr/bin/python
# -*- coding: utf-8 -*-
from config import *
import ntplib
import requests
import json
from datetime import datetime


def utc_now():
    x = ntplib.NTPClient()
    return str(datetime.utcfromtimestamp(x.request('th.pool.ntp.org').tx_time)).replace(' ', 'T')[:23] + 'Z'


def wprint(uid, *args):
    title = ''
    ext = ''
    for i in args:
        if args.index(i) == 0:
            title += str(i) + ' '
        else:
            ext += str(i) + ' '
    try:
        requests.post(STAT_CONSUMER, data=json.dumps(dict(id=uid, stat_message=title, ext_stat_message=ext)))
    except:
        pass
