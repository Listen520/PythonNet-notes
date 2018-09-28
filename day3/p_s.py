from socket import *
from select import *

s = socket()
s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
s.bind(('0.0.0.0',8888))
s.listen(5)

p = poll()

fdmap = {s.fileno():s}

p.register(s,POLLIN | POLLERR)

while True:
    events = p.poll()
    for fd,event in events:
        if fd == s.fileno():
            c,addr = fdmap[fd].accept()
            print('Connect from',addr)
            p.register(c,POLLIN | POLLHUP)
            fdmap[c.fileno()] = c
        elif event & POLLIN:
            data = fdmap[fd].recv(1024)
            if not data:
                p.unregister(fdmap[fd])
                fdmap[fd].colse()
                del fdmap[fd]
            else:
                print(data.decode())
                fdmap[fd].send(b'receive')

