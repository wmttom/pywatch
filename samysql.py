#coding:utf-8
import eventlet
import MySQLdb
import ujson

from eventlet.green import zmq
from eventlet import db_pool

eventlet.monkey_patch()
cp = db_pool.ConnectionPool(MySQLdb, max_size=500, host='192.168.1.222', user='tom' ,passwd='6543120', db='pywatch', use_unicode=True, charset="utf8")
context = zmq.Context()
receiver = context.socket(zmq.PULL)
receiver.bind("tcp://*:1800")
pool = eventlet.GreenPool(1000)

def run(recv):
    sql_dict = ujson.loads(recv)
    num = 0
    while num < 10:
        try:
            db = cp.get()
        except Exception, e:
            num += 1
            print e
        else:
            db.autocommit(True)
            connect = db.cursor()
            if sql_dict['value']:
                connect.execute(sql_dict['sql'], sql_dict['value'])
            else:
                connect.execute(sql_dict['sql'])
            cp.put(db)
            print sql_dict['sql']
            break

print "ready"
while True:
    recv = receiver.recv()
    pool.spawn_n(run, recv)