import os
from sys import platform
from multiprocessing import Process
import subprocess
from ivrs_utils import killtree
import constants
import logging
logger = logging.getLogger('rootLogger')

audioRecordingsPath = os.path.join(constants.ROOTPATH,'audioRecordings')
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
    cmdToRun = None
    if not isinstance(filenames, list):
        logger.debug('filenames should be a list returning')

    if not filenames:
        logger.critical("filenames List is empty")
        return None

    for filename in filenames:
        if not os.path.isfile(filename):
            logger.debug ("word File not exist - %s",filename)
            break

    if platform in ["linux","linux2"]:
        filenameList = filenames
        filenames = ' '.join(filenames)
        #cmdToRun = '/usr/bin/vlc %s --volume-step 256 --play-and-exit --no-osd -Idummy' % (filenames)
        #cmdToRun = '/usr/bin/vlc %s --volume-step 256 --play-and-exit --no-osd >>/dev/null 2>&1' % (filenames)
        #cmdToRun = '/usr/bin/mpg123 -b 1024  %s >>/dev/null 2>&1' % (filenames)
        
        cmdToRun = ['/usr/bin/mpg123','-m' ,'-b', '512','-o','pulse', '-q'] + filenameList
        #cmdToRun = '/usr/bin/mpg123 -b 1024  %s ' % (filenames)
    elif platform == "win32":
        filenames = [filename.replace('\\','\\\\') for filename in filenames]
        filenames = ' '.join(filenames)
        cmdToRun = 'C:\\Program^ Files^ ^(x86)\\VideoLAN\\VLC\\vlc.exe %s --play-and-exit --no-osd' % (filenames)
        logger.debug(cmdToRun)

    return cmdToRun

def playAllTracks(cmdToRun):
    ret = None
    try:
        ret = subprocess.check_output(cmdToRun,shell=False, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        logger.debug('exception in PlayAllTracks - %s',str(e))

    #ret = os.system(cmdToRun)
    logger.debug(ret == os.EX_OK)


currProcess = None

def waitForJoin():
    global currProcess
    if currProcess and currProcess.is_alive():
        logger.debug('waiting to Join')
        currProcess.join()
    else:
        currProcess = None

def stopNonBlockingProcess():
    global currProcess
    if currProcess:
        logger.debug('trying to terminate - %s', str(currProcess.pid))
        #subprocess.Popen(['vlc-ctrl',  'volume',  '+10%'])
        if currProcess.is_alive():
            # try:
            #     # subprocess.Popen(['vlc-ctrl',  'stop'])
            # except Exception:
            #     pass
            logger.debug('terminating - %s', str(currProcess.pid))
            # currProcess.terminate()
            killtree(currProcess.pid)
    else:
        logger.debug('invalid currProcess %s', str(currProcess))


def startNonBlockingProcess(filenames,isBlocking=False,targetProcess=playAllTracks):
    global currProcess
    #logger.debug('inside startNB')
    stopNonBlockingProcess()
    externalCmd =  getExternalCmd(filenames)
    p = Process(target=targetProcess,args=(externalCmd,))
    #p.daemon = True
    p.start()
    currProcess = p
    logger.debug('process in run: %s',  str(currProcess.pid))
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
        week_filename = constants.WEEKDAYS_HINDI[datetime_obj.weekday()] + '.mp4'
        week_filename = key2fileWithoutMap(week_filename)
        dateFileList = [week_filename] + dateFileList

    return dateFileList
