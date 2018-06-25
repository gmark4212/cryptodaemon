#!/usr/bin/python
# -*- coding: utf-8 -*-
import ntplib
from datetime import datetime


def utc_now():
    x = ntplib.NTPClient()
    return str(datetime.utcfromtimestamp(x.request('th.pool.ntp.org').tx_time)).replace(' ', 'T')[:23] + 'Z'