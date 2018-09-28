from socket import * 
import os,sys 
import signal 

#创建套接字
HOST = "0.0.0.0"
PORT = 8888
ADDR = (HOST,PORT)

def client_handler(c):
    print("Connect from ",c.getpeername())
    try:
        while True:
            data = c.recv(1024)
            if not data:
                break 
            print(data)
            c.send(b"Receive your message")
    except (KeyboardInterrupt,SystemExit):
        sys.exit("退出进程")
    except Exception as e:
        print(e)
    c.close()
    sys.exit(0) #子进程结束


s = socket()
s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
s.bind(ADDR)
s.listen(5)

print("Parent process wait connect")
#对僵尸进程处理
signal.signal(signal.SIGCHLD,signal.SIG_IGN)

while True:
    try:
        c,addr = s.accept()
    except KeyboardInterrupt:
        s.close()
        sys.exit("服务器退出")
    except Exception as e:
        print(e)
        continue
    #创建子进程处理客户端请求
    pid = os.fork()

    if pid == 0:
        s.close()
        #处理客户端请求
        client_handler(c)
    else:
        c.close()
        continue

