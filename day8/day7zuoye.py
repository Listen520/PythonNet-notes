import multiprocessing as mp 
from signal import * 
import os,sys
from time import sleep 

#子进程出处理信号
def saler_handler(sig,frame):
    if sig == SIGINT:
        os.kill(os.getppid(),SIGUSR1)
    elif sig == SIGQUIT:
        os.kill(os.getppid(),SIGUSR2)
    elif sig == SIGUSR1:
        print("到站了，请下车")
        sys.exit('售票员下车了')

def driver_handler(sig,frame):
    if sig == SIGUSR1:
        print("老司机，开车了")
    elif sig == SIGUSR2:
        print("车速有点快，系好安全带")
    elif sig == SIGTSTP:
        os.kill(p.pid,SIGUSR1)

#创建子进程表示售票员
def saler():
    while True:
        signal(SIGINT,saler_handler)
        signal(SIGQUIT,saler_handler)
        signal(SIGUSR1,saler_handler)
        signal(SIGTSTP,SIG_IGN)
        sleep(2)
        print("准备好，带你去远方看晴空万里")

p = mp.Process(target = saler)
p.start()

while True:
    if p.is_alive() is False:
        sys.exit('老司机下车了')
    signal(SIGUSR1,driver_handler)
    signal(SIGUSR2,driver_handler)
    signal(SIGTSTP,driver_handler)
    signal(SIGINT,SIG_IGN)
    signal(SIGQUIT,SIG_IGN)

p.join()