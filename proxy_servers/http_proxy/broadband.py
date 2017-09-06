#!/usr/bin/env python
# encoding=utf-8
import os
import time
import requests
import traceback
import socket
import struct
import fcntl


servers_url = ''

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', 'ppp0'))[20:24])
def try_number(num, second):
    def _func(func):
        def __func(*args, **kwargs):
            loop = 0
            while 1:
                loop += 1
                try:
                    return func(*args, **kwargs)
                except:
                    print traceback.print_exc()
                    time.sleep(second)
                    if loop == num:
                        return ''
                        pass

        return __func

    return _func

@try_number(10000000, 1)
def curl(**kwargs):
    if kwargs.get('data'):
        return requests.post(**kwargs)
    else:
        return requests.get(**kwargs)



while 1:
    html = curl(url=servers_url+'/delete', timeout=3).content
    if html !='delete':
        continue
    local_ip = get_local_ip()
    time.sleep(1)
    os.system("poff -a")
    time.sleep(0.1)
    os.system("pon dsl-provider")
    time.sleep(1)
    passwd = '123456'
    while 1:
        if get_local_ip() != local_ip:
            ip_address = curl(url=servers_url+'/proxy?passwd=%s' % passwd, timeout=1)
        continue
    time.sleep(80)