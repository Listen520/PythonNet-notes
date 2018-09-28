#tcp_server.py
from socket import *

sockfd = socket(AF_INET,SOCK_STREAM)

sockfd.bind(('0.0.0.0',6868))

sockfd.listen(8)

print('Waeting for connect...')
connfd,addr = sockfd.accept()
print('Connect from',addr)

while True:
    data = connfd.recv(1024).decode()
    if data == '##':
        break
    print(data)
    n = connfd.send(b'Receive your message')
    print('发送了%d个字节'%n)

connfd.close()
sockfd.close()