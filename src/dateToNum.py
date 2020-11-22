import os
from sys import platform
from multiprocessing import Process, Value, Array
import threading,time,os,signal

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
    'retry':'retry.mp4'
}

def key2file(key):
    return os.path.join(audioRecordingsPath,'hindiaudio',fileKeyMapping[key]) 
    # return './hindiaudio/' + fileKeyMapping[key]

def key2fileWithoutMap(key):
    return os.path.join(audioRecordingsPath,'hindiaudio',key) 

# def getFileFromNum(wordToConvert):
#     dirname = './hindinumbers/'
#     return dirname + wordToConvert + '_hindi.mp3'

def playAllTracks(filenames):
    if not isinstance(filenames, list):
       print('filenames should be a list returning')
       return

    for filename in filenames:
        if os.path.isfile(filename):
            print ("File exist")
        else:
            print ("word File not exist")
            return

    if platform == "linux" or platform == "linux2":
        filenames = ' '.join(filenames)
        cmdToRun = 'vlc  %s  --play-and-exit --no-osd > /dev/null 2>&1' % (filenames)
    elif platform == "win32":
        filenames = [filename.replace('\\','\\\\') for filename in filenames]
        filenames = ' '.join(filenames)
        cmdToRun = 'C:\\Program^ Files^ ^(x86)\\VideoLAN\\VLC\\vlc.exe %s --play-and-exit --no-osd' % (filenames)
        print(cmdToRun)
    os.system(cmdToRun)

currProcess = None
def startNonBlockingProcess(filenames,targetProcess=playAllTracks):
    print('inside startNB')
    global currProcess
    if currProcess != None:
        print('terminating')
        currProcess.kill()
        # os.kill(currProcess.pid,signal.SIGTERM)
        # currProcess.terminate() 
    p = Process(target=targetProcess,args=(filenames,))
    currProcess = p
    #p.daemon = True
    p.start()
    # p.join()

# def date2audioFiles_old(bookDate):
#     from datetime import datetime
#     datetime_obj = datetime.strptime(bookDate,'%d-%B-%Y')

#     #print(numToWords(13))
#     day = numToWords(int(datetime_obj.day),False)
#     month = datetime_obj.strftime('%B')
#     year = numToWords(int(datetime_obj.year),False)

#     dateFileList = day + [month] + year
#     dateFileList = [getFileFromNum(x) for x in dateFileList]
#     #dateFileList = map(getFileFromNum,dateFileList)
#     return dateFileList

def date2audioFiles(bookDate):
    from datetime import datetime
    datetime_obj = datetime.strptime(bookDate,'%d-%B-%Y')
    
    filename = datetime_obj.strftime('%d_%m_%Y') + '.mp4'
    filename = os.path.join(audioRecordingshindiNumbersPath,filename)
    
    dateFileList = [filename]
    return dateFileList



# aa = date2audioFiles('12-April-2019')
# print(aa)
