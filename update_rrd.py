#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Author  : Tiago Bortoletto Vaz <tvaz@riseup.net>
# Updated : Thu Nov  2 22:54:32 UTC 2023

import rrdtool
import urllib.request
import json
import logging

# Toggle this to enable/disable debug output
DEBUG = True

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.WARNING,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("device_monitor.log"),
        logging.StreamHandler()
    ]
)

DEVICES = [
    'http://10.0.0.149',       # FISHINO_1
    'http://10.0.0.100',       # FISHINO_2
    'http://10.0.0.101/json'   # AIRGRADIENT_1
]

def update_db(d):
    try:
        if d['device'] == 'FISHINO_1':
            db = 'fishino_1.rrd'
            rrd_str = f"N:{d['dht11'][0]['temp']}:{d['dht11'][0]['humid']}"
        elif d['device'] == 'FISHINO_2':
            db = 'fishino_2.rrd'
            rrd_str = f"N:{d['dht11'][0]['temp']}:{d['dht11'][0]['humid']}"
        elif d['device'] == 'AIRGRADIENT_1':
            db = 'airgradient_1.rrd'
            rrd_str = f"N:{d['temp']}:{d['humid']}:{d['co2']}:{d['pm']}:{d['voc']}:{d['nox']}"
        else:
            logging.warning(f"Unknown device type: {d.get('device')}")
            return

        logging.debug(f"Updating {db} with: {rrd_str}")
        ret = rrdtool.update(db, rrd_str)
        if ret:
            logging.error(f"RRD update failed for {db}: {rrdtool.error()}")
    except Exception as e:
        logging.error(f"Error updating database for device {d.get('device')}: {e}")

def fetch_data(url):
    try:
        with urllib.request.urlopen(url, timeout=10) as u:
            data = json.load(u)
        logging.debug(f"Fetched data from {url}: {data}")
        return data
    except Exception as e:
        logging.error(f"Failed to fetch data from {url}: {e}")
        raise

if __name__ == '__main__':
    for url in DEVICES:
        try:
            data = fetch_data(url)
            update_db(data)
        except Exception:
            logging.warning(f"Skipping device at {url} due to previous errors.")

