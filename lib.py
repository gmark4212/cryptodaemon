#!/usr/bin/python
# -*- coding: utf-8 -*-
from config import *
import ntplib
import requests
from datetime import datetime


def utc_now():
    x = ntplib.NTPClient()
    return str(datetime.utcfromtimestamp(x.request('th.pool.ntp.org').tx_time)).replace(' ', 'T')[:23] + 'Z'


def wprint(uid, *args):
    message = ''
    for i in args:
        message += str(i)
    print(message)
    try:
        requests.post(STAT_CONSUMER, data=dict(id=uid, stat_message=message))
    except:
        pass
