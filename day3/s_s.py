from socket import *
from select import select

s = socket()
s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
s.bind(('0.0.0.0',8888))
s.listen(4)

rlist = [s]
wlist = []
xlist = [s]

while True:
    rs,ws,xs = select(rlist,wlist,xlist)
    for r in rs:
        if r is s:
            c,addr = r.accept()
            print('Connect from',addr)
            rlist.append(c)
        else:
            data = r.recv(1024)
            if not data:
                rlist.remove(r)
                r.close()
            else:
                print(data.decode())
                wlist.append(r)

    for w in ws:
        w.send(b'Receive your message')
        wlist.remove(w)

    for x in xs:
        if x is s:
            s.close()