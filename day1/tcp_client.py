#tcp_client.py
from socket import *

sockfd = socket(AF_INET,SOCK_STREAM)

server_addr = ('127.0.0.1',6868)
sockfd.connect(server_addr)

while True:
    data = input('发送>>')
    sockfd.send(data.encode())
    if data == '##':
        break
    data = sockfd.recv(1024)
    print('接收到：',data.decode())

sockfd.close