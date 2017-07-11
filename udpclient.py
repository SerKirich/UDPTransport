#!/usr/bin/env python3
# coding=utf-8

from threading import Thread
from socket import *

def ask(sock):
    while True:
        try:
            print(sock.recvfrom(1024)[0].decode())
        except:
            pass

class Client:
    def __init__(self):
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.setblocking(False)
    def run(self):
        server_ip = input("Input server ip: ")
        name = input("Name yourself: ")
        self.sock.sendto(b"_Init_", (server_ip, 8080))
        thr = Thread(target = ask, args = (self.sock,))
        thr.start()
        while True:
            data = input()
            if data:
                self.sock.sendto(name.encode() + b"): " + data.encode(), (server_ip, 8080))

if __name__ == '__main__':
    client = Client()
    client.run()
