#!/usr/bin/python
# -*- coding: UTF-8 -*-
from prometheus_client import start_http_server, Metric, REGISTRY
import json
import requests
import sys
import time

class JsonCollector(object):
  def __init__(self):
    pass
    
  def collect(self):
    # Fetch the JSON
    token = 'demo-token-won\'t-work' #apply for a token here: http://aqicn.org/data-platform/token/
    url = 'http://api.waqi.info/feed/'
    city = 'Wrocław' # Cities: http://aqicn.org/city/all/
    response = json.loads(requests.get(url+city+"/?token="+token).content.decode('Utf-8'))

    metric = Metric('aqi_airquality', 'Air Quality Index', 'gauge')
    metric.add_sample('aqi_airquality', value=response['data']['aqi'], labels={})
    yield metric

    metric = Metric('aqi_co', 'CO gases', 'gauge')
    metric.add_sample('aqi_co', value=response['data']['iaqi']['co']['v'], labels={})
    yield metric

    metric = Metric('aqi_humidity', 'Air Humidity', 'gauge')
    metric.add_sample('aqi_humidity', value=response['data']['iaqi']['h']['v'], labels={})
    yield metric

    metric = Metric('aqi_no2', 'NO2 gases', 'gauge')
    metric.add_sample('aqi_no2', value=response['data']['iaqi']['no2']['v'], labels={})
    yield metric

    metric = Metric('aqi_pressure', 'Air Pressure', 'gauge')
    metric.add_sample('aqi_pressure', value=response['data']['iaqi']['p']['v'], labels={})
    yield metric

    metric = Metric('aqi_pm25', 'pm2.5 particles', 'gauge')
    metric.add_sample('aqi_pm25', value=response['data']['iaqi']['pm25']['v'], labels={})
    yield metric

    metric = Metric('aqi_temp', 'Air temperature', 'gauge')
    metric.add_sample('aqi_temp', value=response['data']['iaqi']['t']['v'], labels={})
    yield metric
if __name__ == '__main__':
  # Usage: airq_exporter.py port
  start_http_server(int(sys.argv[1]))
  REGISTRY.register(JsonCollector())

  while True: time.sleep(1)
