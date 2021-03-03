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
    'timeout':'timeout.mp4',
    'bookInstr':'booking_instruction.mp4'
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
        cmdToRun = '/usr/bin/vlc %s --volume-step 256 --play-and-exit --no-osd >>/dev/null 2>&1' % (filenames)
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

currProcess = None
def waitForJoin():
    global currProcess
    if currProcess and currProcess.is_alive():
        currProcess.join()
    else:
        currProcess = None

def stopNonBlockingProcess():
    global currProcess
    if currProcess:
        print('terminating - ' + str(currProcess.pid))
        #subprocess.Popen(['vlc-ctrl',  'volume',  '+10%'])
        if currProcess.is_alive():
            try:
                subprocess.Popen(['vlc-ctrl',  'stop'])
            except Exception:
                pass
            print('terminating - ' + str(currProcess.pid))
            killtree(currProcess.pid)
    else:
        print('invalid currProcess ' + str(currProcess))


def startNonBlockingProcess(filenames,isBlocking=False,targetProcess=playAllTracks):
    #print('inside startNB')
    stopNonBlockingProcess()
    externalCmd =  getExternalCmd(filenames)

    callback_rt = lambda x:keyPressCallback(x,atm)
    callback_rt = lambda x:subprocess.check_output(externalCmd,shell=True)
    register_callback(callback_rt)
    
    ret = subprocess.check_output(externalCmd,shell=True)
    #ret = os.system(cmdToRun)
    print(ret == os.EX_OK)
    p = Process(target=targetProcess,args=(externalCmd,))
    #p.daemon = True
    p.start()
    currProcess = p
    print('process in run:' + str(currProcess.pid))
    if isBlocking:
        p.join()



def date2audioFiles(bookDate):
    from datetime import datetime
    datetime_obj = datetime.strptime(bookDate,'%d-%B-%Y')

    filename = datetime_obj.strftime('%d_%m_%Y') + '.mp4'
    filename = os.path.join(audioRecordingshindiNumbersPath,filename)

    dateFileList = [filename]
    return dateFileList

