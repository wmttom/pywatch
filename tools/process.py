#coding:utf-8
import os

def get_pid():
    dirs = os.listdir("/proc")
    pid_list = []
    for pid in dirs:
        try:
            pid_num = int(pid)
        except Exception, e:
            pass
            #print Exception, e
        else:
            pid_list.append(pid_num)
    return pid_list

def get_name(pid_list):
    name_list = []
    for pid in pid_list:
        pid_file = open("/proc/%s/cmdline" %pid, "rb")
        name = pid_file.read()
        pid_file.close()
        name_list.append(name)
    return name_list

def main(process):
    pid_list = get_pid()
    #print pid_list
    name_list = get_name(pid_list)
    #print name_list
    for name in name_list:
        if name.find(process) >= 0:
            print name
            if name.split("/")[-1].replace("\0", "") == process:
                print "%s is alive."%process
                print "ok"

if __name__ == '__main__':
    main("apache")