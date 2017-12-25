#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import thread
import time
import datetime

def socketServer():
    sockServer = socket.socket()
    sockServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sockServer.bind(('', 49781))
    sockServer.listen(1)
    return sockServer

sockClient = socket.socket()
sockClient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sockClient.bind(('', 49782))
sockClient.listen(1)

def logWrite(message):
    print(message)
    ts = time.time()
    ts = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    with open('/var/log/proxy.log', 'a') as f:
        f.write(ts + " " + message + '\n')


def serverListener(sockServer):
    global connServer
    while True:
        try:
            connServer, addrClient = sockServer.accept()
        except:
            continue
        logWrite('server connected\n')

sockServer = socketServer()
thread.Thread(serverListener, (sockServer,))

while True:
    connClient, addrClient = sockClient.accept()
    if (connClient):
        logWrite('client connected')
        try:
            connServer.send('b')
            connClient.shutdown(socket.SHUT_RDWR)
        except:
#           sockServer.shutdown(socket.SHUT_RDWR)
            connClient.shutdown(socket.SHUT_RDWR)
#           time.sleep(5)
#           sockServer = socketServer()
