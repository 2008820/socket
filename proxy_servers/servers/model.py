#!/usr/bin/env python
# encoding=utf-8
import sqlite3



conn = sqlite3.connect("ipProxy.db", check_same_thread=False)


def creat_table():
    c = conn.cursor()
    c.execute(
        '''CREATE TABLE IF NOT EXISTS ipproxy(ip TEXT PRIMARY KEY , usetimes int DEFAULT 0, update_time TIMESTAMP DEFAULT (datetime('now', 'localtime')))''')
    conn.commit()
    c.close()


def insert_table(ip):
    c = conn.cursor()
    try:
    # c.execute('''update ipproxy set ip='%s', update_time='%s' ''' % (ip, datetime.datetime.now()))
        c.execute('''insert into ipproxy(ip) VALUES ('%s')'''%ip)
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    c.close()


def delete_table(ip):
    c = conn.cursor()
    c.execute('''delete from ipproxy where ip='%s' ''' % ip)
    conn.commit()
    c.close()


def get_one():
    c = conn.cursor()
    c.execute('SELECT ip,usetimes FROM ipproxy order by update_time DESC LIMIT 1')
    ip = c.fetchone()
    c.close()
    if ip:
        return ip
    else:
        return ('', '')

def count_ip(ip, times):
    c = conn.cursor()
    times += 1
    c.execute("update ipproxy set usetimes=%d where ip='%s' "% (times, ip))
    conn.commit()
    return

def get_all():
    c = conn.cursor()
    c.execute('SELECT * from ipproxy')
    result = c.fetchall()
    return result

creat_table()

if __name__ == '__main__':
    pass