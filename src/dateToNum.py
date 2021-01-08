import os
from sys import platform
from multiprocessing import Process, Value, Array
import threading,time,os,signal,subprocess
from ivrs_utils import killtree

rootPath = os.path.join(os.getcwd(),'..')
audioRecordingsPath = os.path.join(rootPath,'audioRecordings')
audioRecordingshindiNumbersPath = os.path.join(audioRecordingsPath,'hindidates')

fileKeyMapping = {'welcomeState1':'welcomeStateMsg.mp4',
    'keliye':'keliye.mp4',
    'dabayein':'dabayein.wav',
    'confirmState1':'confirmState1.mp4',
    'confirmState2':'confirmState2.mp4',
    'alreadyState1':'alreadyState1.mp4',
    'alreadyState2':'alreadyState2.mp4',
    'booked':'booked.mp4',
    'callback':'callback.mp4',
    'cancelled':'cancelled.mp4',
    'retry':'retry.mp4',
    'timeout':'timeout.mp4'
}

def key2file(key):
    return os.path.join(audioRecordingsPath,'hindiaudio',fileKeyMapping[key]) 
    # return './hindiaudio/' + fileKeyMapping[key]

def key2fileWithoutMap(key):
    return os.path.join(audioRecordingsPath,'hindiaudio',key) 

def getExternalCmd(filenames):
    if not isinstance(filenames, list):
       print('filenames should be a list returning')
       return

    for filename in filenames:
        if not os.path.isfile(filename):
            print ("word File not exist - " + filename)
            return

    if platform == "linux" or platform == "linux2":
        filenames = ' '.join(filenames)
        #cmdToRun = '/usr/bin/vlc %s --volume-step 256 --play-and-exit --no-osd -Idummy' % (filenames)
        cmdToRun = '/usr/bin/vlc %s --volume-step 256 --play-and-exit --no-osd' % (filenames)
    elif platform == "win32":
        filenames = [filename.replace('\\','\\\\') for filename in filenames]
        filenames = ' '.join(filenames)
        cmdToRun = 'C:\\Program^ Files^ ^(x86)\\VideoLAN\\VLC\\vlc.exe %s --play-and-exit --no-osd' % (filenames)
        print(cmdToRun)
    return cmdToRun

def playAllTracks(cmdToRun):
    #TODO:try catch here
    ret = subprocess.check_output(cmdToRun,shell=True)
    #ret = os.system(cmdToRun)
    
    print(ret == os.EX_OK)


currNonBlockingProcess=None
def startNonBlockingProcess4(filenames):
    global currNonBlockingProcess

    if currNonBlockingProcess:
        killtree(currNonBlockingProcess)
        currNonBlockingProcess = None

    externalCmd = getExternalCmd(filenames) + ' & echo $!'
    currNonBlockingProcess = subprocess.check_output(externalCmd,shell=True)
    print('what call returned--')
    print(str(currNonBlockingProcess))
    #p1 = subprocess.Popen(externalCmd,stderr=subprocess.STDOUT, stdout=subprocess.PIPE, text=True)
    #currNonBlockingProcess = p1.pid
    print('runnig process')


def startNonBlockingProcess3(filenames):
    global currNonBlockingProcess

    if currNonBlockingProcess:
        killtree(currNonBlockingProcess)
        currNonBlockingProcess = None

    externalCmd = getExternalCmd(filenames).split()
    p1 = subprocess.Popen(externalCmd,stderr=subprocess.STDOUT, stdout=subprocess.PIPE, text=True)
    currNonBlockingProcess = p1.pid
    print('runnig process')


currProcess = None
def waitForJoin():
    if currProcess:
        currProcess.join()


def startNonBlockingProcess(filenames,targetProcess=playAllTracks):
    #print('inside startNB')
    global currProcess
    if currProcess != None:
        print('terminating - ' + str(currProcess))
        #currProcess.kill()
        #subprocess.Popen(['vlc-ctrl',  'volume',  '+10%'])
        subprocess.Popen(['vlc-ctrl',  'pause'])
        if currProcess.is_alive():
            print('terminating - ' + str(currProcess.pid))
            killtree(currProcess.pid)
    else:
        print('invalid currProcess ' + str(currProcess))
    
    externalCmd =  getExternalCmd(filenames)
    p = Process(target=targetProcess,args=(externalCmd,))
    #p.daemon = True
    p.start()
    currProcess = p
    print('process in run:' + str(currProcess.pid))
    # p.join()



def date2audioFiles(bookDate):
    from datetime import datetime
    datetime_obj = datetime.strptime(bookDate,'%d-%B-%Y')

    filename = datetime_obj.strftime('%d_%m_%Y') + '.mp4'
    filename = os.path.join(audioRecordingshindiNumbersPath,filename)

    dateFileList = [filename]
    return dateFileList

