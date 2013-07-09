#coding:utf-8
import os

def disk_info():
    info_list = os.statvfs("/")
    disk_dict = {}
    # MB
    disk_dict['total'] = info_list.f_frsize * info_list.f_blocks / (1024 * 1024.0)
    disk_dict['free'] = info_list.f_frsize * info_list.f_bfree / (1024 * 1024.0)
    disk_dict['avail'] = info_list.f_frsize * info_list.f_bavail / (1024 * 1024.0)
    disk_dict['used'] = disk_dict['total']  - disk_dict['free']
    #print disk_dict['used'] / float(disk_dict['total']) / 0.95
    return disk_dict

if __name__ == '__main__':
    print disk_info()