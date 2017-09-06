#!/usr/bin/env python
# encoding=utf-8
import requests
from client.client import proxy_client

@proxy_client
def curl(**kwargs):
    proxy = curl.func_dict['proxy']
    if kwargs.get('data'):
        return requests.post(proxies={'http': proxy}, **kwargs)
    else:
        return requests.get(proxies={'http': proxy}, **kwargs)

print curl(url='http://ip.cn').content