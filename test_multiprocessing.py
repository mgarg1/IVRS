

from multiprocessing import Process, Value, Array
import threading

import time

currProcess = None


def f1():
    cnt = 0
    while cnt < 20 :
        print('I am in f1')
        time.sleep(2)
        cnt += 1

def startProcess2(num):
    global currProcess
    if num == '1':
        if currProcess != None:
            currProcess.kill()
        
        p = threading.Thread(target=f1)
        currProcess = p
        p.daemon = True
        p.start()
        #p.join()



def startProcess(num):
    global currProcess
    if num == '1':
        if currProcess != None:
            currProcess.terminate() 
        p = Process(target=f1)
        currProcess = p
        #p.daemon = True
        p.start()
        #p.join()



def main():

    while True:
        aa = input('enter process number:')
        startProcess(aa)


main()
