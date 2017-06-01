#!/usr/bin/env python
# encoding=utf-8
import socket
import re
import threading


def run():
    while True:
        conn, address = s.accept()
        conn_thread = threading.Thread(target=handler_conn, args=(conn,))
        conn_thread.start()

def handler_conn(conn):
    alldata = ''
    while 1:
        data = conn.recv(1024)
        alldata = alldata + data
        try:
            content_lenth = re.findall('Content-Length:[\s\S]*?(\d+)', alldata)[0]
        except:
            content_lenth = 0
        if data.endswith('\r\n\r\n') and content_lenth == 0:
            break
        else:
            if len(alldata.split('\r\n')[-1]) == int(content_lenth):
                break
    methon_url = alldata.split('\n')[0].split(' ')
    methon, url = methon_url[0], methon_url[1]
    host_port = url.replace('http://', "").split('/')[0].split(":")
    host = host_port[0]
    port = 80 if len(host_port) == 1 else host_port[1]
    target_s = socket.socket()

    target_s.settimeout(20)
    target_s.connect((host, int(port)))
    print "connect"
    if methon == "CONNECT":
        conn.send("HTTP/1.1 200 Connection established\r\nConnection: close\r\n\r\n")
    else:
        target_s.send(alldata)

    print 'get data'
    t1 = threading.Thread(target=dock_socket, args=(conn, target_s, False))
    t2 = threading.Thread(target=dock_socket, args=(target_s, conn, True))
    t1.start()
    t2.start()



def dock_socket(recv, send, recv_from_response=False):
    try:
        while True:
            buf = recv.recv(1024*4)
            if not recv_from_response:
                print '*' * 100
                print buf
            send.send(buf)
            if not buf:
                break
    except Exception, e:
        recv.close()
        send.close()
        return
    if recv_from_response:
        recv.close()
        send.close()

if __name__ == "__main__":
    import argparse
    description = "http/https proxy, -p prot default 11112 "
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-p", help="prot num", default=11112)
    args = parser.parse_args()
    PORT = int(args.p)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", PORT))
    s.listen(5)
    print("监听开始了")
    try:
        run()
    except Exception, e:
        s.close()
        exit(e)


