#coding:utf-8
import ujson
import zmq

context = zmq.Context()
receiver = context.socket(zmq.PULL)
receiver.bind("tcp://*:1728")

sender = context.socket(zmq.PUSH)
sender.connect("tcp://127.0.0.1:1800")

def get_save_info(info):
    save_dict = {}
    save_dict['sql'] = "INSERT INTO pywatch VALUES (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\
                                %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,FROM_UNIXTIME(%s))"
    info_list = (info['host'], info['cpu_load']['process_count'], info['cpu_load']['1m'], info['cpu_load']['5m'],\
                      info['cpu_load']['15m'], info['cpu_rate']['total'], info['cpu_rate']['user'], info['cpu_rate']['system'],\
                      info['cpu_rate']['iowait'], info['mem']['app_used'], info['mem']['os_used'], info['mem']['total'],\
                      info['disk_used']['avail'], info['disk_used']['used'], info['disk_used']['total'], info['disk_io']['rps'],\
                      info['disk_io']['wps'], info['disk_io']['rkb'], info['disk_io']['wkb'], info['net_io']['in_byte_rate'],\
                      info['net_io']['out_byte_rate'], info['net_io']['in_packets_rate'], info['net_io']['out_packets_rate'],\
                      info['timestamp'])
    save_dict['value'] = info_list
    return save_dict

print "ready"
while True:
    recv = receiver.recv()
    info = ujson.loads(recv)
    print info
    save_dict = get_save_info(info)
    sender.send(ujson.dumps(save_dict))