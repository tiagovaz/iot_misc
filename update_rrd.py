#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Author  : Tiago Bortoletto Vaz <tvaz@riseup.net>
# Updated : Thu Nov  2 22:54:32 UTC 2023


import rrdtool
import urllib.request, json 

DEVICES = ['http://10.0.0.126', # FISHINO_1
           'http://10.0.0.127', # FISHINO_2
           'http://10.0.0.128/json'] # AIRGRADIENT_1

DEBUG = False

def update_db(d):
    if DEBUG is True:
        print(d)
    if d['device'] == 'FISHINO_1':
        db = 'fishino_1.rrd'
        rrd_str = 'N:%s:%s' % (d['dht11'][0]['temp'], d['dht11'][0]['humid'])
    elif d['device'] == 'FISHINO_2':
        db = 'fishino_2.rrd'
        rrd_str = 'N:%s:%s' % (d['dht11'][0]['temp'], d['dht11'][0]['humid'])
    elif d['device'] == 'AIRGRADIENT_1':
        db = 'airgradient_1.rrd'
        rrd_str = 'N:%s:%s:%s:%s' % (d['temp'], d['humid'], d['co2'], d['pm'])
    ret = rrdtool.update(db, rrd_str);
    if DEBUG is True:
        print(rrd_str)

def fetch_data(url):
    with urllib.request.urlopen(url) as u:
        data = json.load(u)
    return data

if __name__ == '__main__':
    for url in DEVICES:
        data = fetch_data(url)
        update_db(data)
