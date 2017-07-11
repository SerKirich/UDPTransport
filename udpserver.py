#!/usr/bin/env python3
# coding=utf-8

from socket import *
import getip

class Server:
    def __init__(self):
        self.addrs = []
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.setblocking(False)
        self.sock.bind(("", 8080))
    def run(self):
        print("UDPServer started on {}...".format(getip.getip()))
        while True:
            try:
                data, addr = self.sock.recvfrom(1024)
            except:
                continue
            if not addr in self.addrs:
                self.addrs.append(addr)
            if data not in (b"_Init_", b"_Exit_"):
                for each_addr in self.addrs:
                    if each_addr != addr:
                        try:
                            self.sock.sendto(addr[0].encode() + b" (" + data, each_addr)
                        except:
                            print("Address {} is not available.".format(each_addr))
            elif data == b"_Init_":
                self.sock.sendto(b"Thankyou for joining the chat!", addr)
            elif data == b"_Exit_":
                for i in range(self.addrs):
                    if self.addrs[i] == addr:
                        del self.addrs[i]
            print(addr[0].encode() + b" (" + data)

if __name__ == '__main__':
    server = Server()
    server.run()
