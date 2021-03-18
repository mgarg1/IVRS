import os
from sys import platform
from multiprocessing import Process, Value, Array
import threading,time,os,signal,subprocess
from ivrs_utils import killtree
from constants import WEEKDAYS_HINDI

rootPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# rootPath = os.path.join(os.getcwd(),'..')
audioRecordingsPath = os.path.join(rootPath,'audioRecordings')
audioRecordingshindiNumbersPath = os.path.join(audioRecordingsPath,'hindidates')

fileKeyMapping = {'welcomeState1':'welcomeStateMsg.mp4',
    'keliye':'keliye.mp4',
    'dabayein':'dabayein.mp4',
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
        print('waiting to Join')
        currProcess.join()
    else:
        currProcess = None

def stopNonBlockingProcess():
    global currProcess
    if currProcess:
        print('trying to terminate - ' + str(currProcess.pid))
        #subprocess.Popen(['vlc-ctrl',  'volume',  '+10%'])
        if currProcess.is_alive():
            try:
                subprocess.Popen(['vlc-ctrl',  'stop'])
            except Exception:
                pass
            print('terminating - ' + str(currProcess.pid))
            # currProcess.terminate()
            killtree(currProcess.pid)
    else:
        print('invalid currProcess ' + str(currProcess))


def startNonBlockingProcess(filenames,isBlocking=False,targetProcess=playAllTracks):
    global currProcess
    #print('inside startNB')
    stopNonBlockingProcess()
    externalCmd =  getExternalCmd(filenames)
    p = Process(target=targetProcess,args=(externalCmd,))
    #p.daemon = True
    p.start()
    currProcess = p
    print('process in run:' + str(currProcess.pid))
    if isBlocking:
        p.join()



def date2audioFiles(bookDate,includeYear=False,includeDayOfWeek=False):
    from datetime import datetime
    datetime_obj = datetime.strptime(bookDate,'%d-%B-%Y')

    date_filename = datetime_obj.strftime('%d_%m') + '.mp4'
    date_filename = os.path.join(audioRecordingshindiNumbersPath,date_filename)

    dateFileList = [date_filename]
    if includeYear:
        year_filename = datetime_obj.strftime('%Y') + '.mp4'
        year_filename = os.path.join(audioRecordingshindiNumbersPath,year_filename)
        dateFileList += [year_filename]
    
    if includeDayOfWeek:
        #TODO: use key to file mapping for weekdays
        week_filename = WEEKDAYS_HINDI[datetime_obj.weekday()] + '.mp4'
        week_filename = key2fileWithoutMap(week_filename)
        dateFileList = [week_filename] + dateFileList

    return dateFileList