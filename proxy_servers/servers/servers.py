#!/usr/bin/env python
# encoding=utf-8
import json
from flask import Flask, request
from model import get_one, delete_table, insert_table, get_all, count_ip

app = Flask(__name__)
proxy_port = ':11113'
server_port = 5111


@app.route('/')
def index():
    return "代理ip地址:[], 端口号 11113"


@app.route('/proxy')
def send_proxy():
    passwd = request.args.get('passwd')
    if passwd == '123456':
        temp_proxy = request.remote_addr + proxy_port
        insert_table(temp_proxy)
        return request.remote_addr
    return 'no route'


@app.route('/delete')
def delete_ip():
    temp_proxy = request.remote_addr + proxy_port
    print temp_proxy
    delete_table(temp_proxy)
    return 'delete'


@app.route('/getall')
def get_ip():
    return json.dumps(get_all())


@app.route('/getone')
def get_one_ip():
    ip, times = get_one()
    if not ip:
        return ''
    count_ip(ip, times)
    return ip


if __name__ == '__main__':
    app.run('0.0.0.0', server_port, debug=True)
