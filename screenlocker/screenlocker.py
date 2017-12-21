import socket
import time
import datetime
import ctypes


def logWrite(logText):
    ts = time.time()
    ts = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    logText = ts + " " + logText + '\n'
    print(logText)
#    with open('C:\\temp\\screenlocker.log', 'a') as f:
#        f.write(logText)

def connect():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('noip.zenden.ru', 49781))
    sock.settimeout(120)

logWrite('screen locker running...')

while True:
    try:
        connect()
    except socket.error:
        print
        ('socket error')
        continue
    logWrite('connected')
    try:
        data = sock.recv(1024)
    except:
#        sock.shutdown(socket.SHUT_RDWR)
        continue
    if not data:
#        sock.shutdown(socket.SHUT_RDWR)
        continue        
    if 'b' in str(data):
        logWrite('got lock signal')
        ctypes.windll.user32.LockWorkStation()