#!/usr/bin/env python
# encoding=utf-8
import time
import traceback
import requests
from requests.exceptions import ProxyError, ReadTimeout, ConnectionError
from functools import wraps, update_wrapper

__all__ =['proxy_client']
PROXY_SERVER = ''


class ServerError(Exception):
    def __init__(self, vaule):
        self.vaule = vaule

    def __str__(self):
        return repr('Server Error - %s' % self.vaule)

class ProxyClient(object):
    def __init__(self):
        self.proxy_server = PROXY_SERVER
        self.loop = 10
        self.get_loop = 10
        self.passwd = '1qaz2wsx'

    def get_one_ip(self):
        while 1:
            try:
                content = requests.get(self.proxy_server + '/getone', timeout=20).content
            except Exception, e:
                raise ServerError(e)
            if content:
                return content
            else:
                print 'ip无法获取到'
                time.sleep(1)
                continue

    def get_all_ip(self):
        content = requests.get(self.proxy_server + '/getall').json()
        return content

    def __call__(self, func):
        func.__dict__['proxy'] = self.get_one_ip()
        @wraps(func)
        def __call(*args, **kwargs):
            while 1:
                num = 0
                num += 1
                try:
                    result = func(*args, **kwargs)
                    return result
                except ProxyError:
                    # traceback.print_exc()
                    print 'change IP proxy - proxy-error'
                    time.sleep(2)
                    func.__dict__['proxy'] = self.get_one_ip()
                    update_wrapper(__call, func)
                    wraps(func)
                except ReadTimeout:
                    # traceback.print_exc()
                    print 'change IP proxy readtimeout-error'
                    time.sleep(2)
                    func.__dict__['proxy'] = self.get_one_ip()
                    update_wrapper(__call, func)
                    wraps(func)
                except ConnectionError:
                    if num == self.loop:
                        raise ServerError(func.func_dict)
                    traceback.print_exc()
                    print 'change IP proxy'
                    time.sleep(2)
                    func.__dict__['proxy'] = self.get_one_ip()
                    update_wrapper(__call, func)
                    wraps(func)

        return __call


proxy_client = ProxyClient()

if __name__ == '__main__':
    @proxy_client
    def curl(self, **kwargs):
        proxy = self.curl.func_dict['proxy']
        self.crawler.logger.info('use proxy ip is %s'%proxy)
        if kwargs.get('data'):
            return self.req.post(proxies={'http': proxy}, **kwargs)
        else:
            return self.req.get(proxies={'http': proxy}, **kwargs)
    html = curl.get('http://www.baidu.com').content