#coding:utf-8
import time
import ujson
import zmq

from tools import cpu_load
from tools import cpu_rate
from tools import mem
from tools import disk_used
from tools import disk_io
from tools import net_io

TIME_INTERVAL = 60
MASTER_IP = "192.168.1.227"
CLIENT_INFO = "220"

context = zmq.Context()
sender = context.socket(zmq.PUSH)
sender.connect("tcp://%s:1728"%MASTER_IP)

def get_info():
    info_dict = {}
    info_dict['cpu_load'] = cpu_load.cpu_load()
    info_dict['mem'] = mem.mem_info()
    info_dict['disk_used'] = disk_used.disk_info()
    info_dict['cpu_rate'] = cpu_rate.cpu_info()
    info_dict['disk_io'] = disk_io.disk_io()
    info_dict['net_io'] = net_io.net_info()
    return info_dict

def get_result(start, end):
    result = {}
    result['cpu_load'] = end['cpu_load']
    result['mem'] = end['mem']
    result['disk_used'] = end['disk_used']
    result['cpu_rate'] = cpu_rate.cpu_rate(start['cpu_rate'], end['cpu_rate'])
    result['disk_io'] = disk_io.io_rate(start['disk_io'], end['disk_io'], TIME_INTERVAL)
    result['net_io'] = net_io.net_rate(start['net_io'], end['net_io'], TIME_INTERVAL)
    return result

def main():
    start = get_info()
    global TIME_INTERVAL
    time_start = time.time()    
    while True:
        time.sleep(TIME_INTERVAL)
        end = get_info()
        time_end = time.time()
        if int(time_end - time_start) != 60:
            TIME_INTERVAL = 60 - int(time_end - time_start) + 60
            ts = time_end - int(time_end - time_start) + 60
            print TIME_INTERVAL
        else:
            TIME_INTERVAL = 60
            ts = time_end
        time_start = ts
        send_dict = get_result(start, end)
        send_dict['timestamp'] = ts
        print ts
        send_dict['host'] = CLIENT_INFO
        sender.send(ujson.dumps(send_dict))
        start = end


if __name__ == '__main__':
    main()