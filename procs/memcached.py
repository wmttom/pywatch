#coding:utf-8
import socket

HOST = ("192.168.1.166",11211)

def get_status():
    mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mysock.connect(HOST)
    mysock.send("stats")
    mysock.send('\r\n')
    result = mysock.recv(65535)
    lines = result.split("\r\n")
    result_dict = [{line.split()[1]:line.split()[2]} for line in lines if line.find(" ")>0]
    print result_dict

if __name__ == "__main__":
    get_status()