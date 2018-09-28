#!/usr/bin/env python3
#coding=utf-8

'''
name:ChenHongwei
enail:chenhongwei680@126.com
date:2018-9
class:AID
introduce:Chatroom server
env:python3.5
'''
from socket import *
import os,sys

#接收客户端请求
def do_parent(s):
    d = {}
    while True:
        msg,addr = s.recvfrom(1024)
        msgList = msg.decode().split(' ')

        #区分请求类型
        if msgList[0] == 'L':
            do_login(s,d,msgList[1],addr)
        elif msgList[0] == 'C':
            do_chat(s,d,msgList[1],' '.join(msgList[2:]))
        elif msgList[0] == 'Q':
            do_quit(s,d,msgList[1])

#做管理员喊话
def do_child(s,addr):
    while True:
        m = input('管理员消息：')
        m = 'C 管理员 ' + m
        s.sendto(m.encode(),addr)

#记录客户姓名并告知其进入聊天室
def do_login(s,d,name,addr):
    #判断名字是否已经存在
    if (name in d) or name == '管理员':
        s.sendto('该用户已存在，请重新输入'.encode,addr)
        return
    s.sendto(b'OK',addr)
    #通知其他人
    m = '\n欢迎　%s 进入聊天室'%name
    for i in d:
        s.sendto(m.encode(),d[i])
    #名字为键，地址为值，放入字典
    d[name] = addr

#其他人都收到消息
def do_chat(s,d,name,text):
    m = '\n%s 说:%s'%(name,text)
    for i in d:
        if i != name:
            s.sendto(m.encode(),d[i])

#退出聊天室
def do_quit(s,d,name):
    m = '\n' + name + '退出了聊天室'
    for i in d:
        if i == name:
            s.sendto(b'EXIT',d[i])
        else:
            s.sendto(m.encode(),d[i])
    #从字典删除用户
    del d[name]

#创建网络，创建进程，调用功能函数
def main():
    #server address
    ADDR = ('0.0.0.0',8888)

    #创建数据报套接字
    s = socket(AF_INET,SOCK_DGRAM)
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)

    #创建一个单独的进程处理管理员喊话功能
    pid = os.fork()
    if pid < 0:
        sys.exit('创建进程失败')
    elif pid == 0:
        do_child(s,ADDR)
    else:
        do_parent(s)


if __name__ == '__main__':
    main()