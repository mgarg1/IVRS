# https://docs.python.org/3/library/subprocess.html#popen-objects

from multiprocessing import Process, Value, Array
import threading,time,os
import subprocess
currProcess = None

def f1(filename):
    cnt = 0

    subprocess.Popen(["python", "test_audio.py",filename])
    
    #os.system('python test_audio.py ' + filename)  
    
    while False:
        print('I am alive ' + filename)
        time.sleep(1)

def startProcess(num):
    global currProcess
    if True:
        if currProcess != None:
            print('killing old process')
            print(currProcess)
            currProcess.terminate()
            #currProcess.join()
            #if currProcess.is_alive():
            #    print('old still alive')
            currProcess = None
        #p = Process(target=f1,args=[num])
        currProcess = subprocess.Popen(["python", "test_audio.py",num])
        #p.daemon = True
        #currProcess = p
        #p.start()
        #p.join()



def main():

    while True:
        aa = input('enter process number:')
        startProcess(aa)


main()
