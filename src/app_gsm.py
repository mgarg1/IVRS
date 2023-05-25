import abc
import os
import threading
from dataAccess import findNextDates, isNumRegistered, storeBooking, cancelBooking
from dateToNum import date2audioFiles, startNonBlockingProcess, stopNonBlockingProcess, key2file, key2fileWithoutMap, waitForJoin
from phoneCmds import registerCallback
from dtmf_decoder3 import read_dtmf, register_callback, remove_callback, gpio_initialize, gpio_clean, gsm_rst, gsm_power_on
from singleton_decorator import singleton
import re
import time
import traceback
# from multiprocessing import shared_memory
from sim800l import SIM800L

import logging
import logging.handlers

logger = logging.getLogger('rootLogger')

SHM_NAME='my_shm68'

atm = None

sim800l=SIM800L('/dev/serial0',9600)
#sim800l=SIM800L('/dev/ttyAMA0')
sim800l.setup()


# import asyncio

# class Timer:
#     def __init__(self, timeout, callback):
#         self._timeout = timeout
#         self._callback = callback
#         self._task = asyncio.ensure_future(self._job())

#     async def _job(self):
#         await asyncio.sleep(self._timeout)
#         await self._callback()

#     def cancel(self):
#         self._task.cancel()

# async def timeout_callback():
#     await asyncio.sleep(0.1)
#     logger.debug('echo! - timeout_callback called')

# def timeout_callback():
#     logger.debug('echo! - timeout_callback called')


class State(object, metaclass = abc.ABCMeta):
    stateMessage = None
    audioList = []
    
    @abc.abstractmethod
    def press1(self, atm):
        self.wrongInput(atm)
    
    @abc.abstractmethod
    def press2(self, atm):
        self.wrongInput(atm)

    def press3(self, atm):
        self.wrongInput(atm)
 
    def press4(self, atm):
        self.wrongInput(atm)
 
    def press5(self, atm):
        self.wrongInput(atm)
 
    def press6(self, atm):
        self.wrongInput(atm)
 
    def press7(self, atm):
        self.wrongInput(atm)
 
    def press8(self, atm):
        self.wrongInput(atm)
 
    def press9(self, atm):
        atm.state = talkState(atm.phoneNum)

    def press0(self, atm):
        self.wrongInput(atm)
    
    def pressStar(self, atm):
        self.wrongInput(atm)

    def pressHash(self, atm):
        self.wrongInput(atm)
    
    def wrongInput(self, atm):
        logger.debug('You have entered a wrong option. Please retry\n')
        atm.state.speak()
        # raise NotImplementedError('')

    def speak(self):
        logger.debug(self.stateMessage)
        #logger.debug(self.audioList)
        startNonBlockingProcess(self.audioList)


class welcomeState(State):
    def __init__(self):
        self.idleTime = 12.0
        self.stateMessage = 'welcome to IVRS: \n1-To Book\n2-To Talk\n'
        # logger.debug('welcome to IVRS: \n1-To Book\n2-To Talk\n')
        self.audioList = [key2file('welcomeState1')]
        self.speak()

    def press1(self, atm):
        atm.state = bookState()

    def press2(self, atm):
        atm.state = talkState(atm.phoneNum)
    
    def press9(self, atm):
        atm.state = talkState(atm.phoneNum)

class talkState(State):
    def __init__(self, phoneNum):
        self.idleTime = 12.0
        self.stateMessage = 'Your callback is registered. You will get a callback soon'
        registerCallback(phoneNum)
        self.audioList = [key2file('callback')]
        self.speak()
        # resMsg='Call karne ke liye dhanywad.Aapse koi representative jald hi contact kerenge. callback_registered'
        # atm.state = exitState(resMsg,phoneNum)
    
    def press1(self, atm):
        pass
    
    def press2(self, atm):
        pass

class bookState(State):
    def __init__(self):
        self.idleTime = 50.0
        self.availDates = findNextDates(numOfDays=8)
        self.stateMessage = 'Booking State:\n'
        self.audioList = [key2file('bookInstr')]
        for x in range(0,len(self.availDates)):
            self.stateMessage += f'Press ' + str(x+1) + ' for ' + self.availDates[x] + '\n'
            self.audioList = self.audioList + self.createAudioList(str(x+1), self.availDates[x])
        self.speak()


    def createAudioList(self,keyNum,availDate):
        #return ['press.wav'] + [getFileFromNum(numToWords(int(keyNum)))] + ['for.wav'] + date2audioFiles(availDate)
        # return date2audioFiles(availDate) + [key2file('keliye')] + [getFileFromNum(numToWords(int(keyNum)))] + [key2file('dabayein')]
        #TODO: have better function than key2fileWithoutMap
        return date2audioFiles(availDate) + [key2file('keliye')] + [key2fileWithoutMap(keyNum + '_dabayein.mp4')]

    def checkKeyPress(self,numPressed,atm):
        atm.state = confirmState(self.availDates[numPressed-1])
    
    def press1(self, atm):
        self.checkKeyPress(1,atm)
    def press2(self, atm):
        self.checkKeyPress(2,atm)
    def press3(self, atm):
        self.checkKeyPress(3,atm)
    def press4(self, atm):
        self.checkKeyPress(4,atm)
    def press5(self, atm):
        self.checkKeyPress(5,atm)
    def press6(self, atm):
        self.checkKeyPress(6,atm)
    def press7(self, atm):
        self.checkKeyPress(7,atm)
    def press8(self, atm):
        self.checkKeyPress(8,atm)

    def press9(self,atm):
        atm.state = talkState(atm.phoneNum)


keepAlive, retVal = True, None

def commonExit(msg,phoneNum):
    logger.debug('inside Common Exit')
    waitForJoin()
    # destroyAll()
    # # can write to someplace
    logger.debug('pid - %s', str(os.getpid()))
    sim800l.end_call()
    if phoneNum:
        sim800l.send_sms(phoneNum,msg)
    # time.sleep(3)
    cleanupAfterCallEnd()
    # global retVal
    # retVal=msg
    # global keepAlive
    # keepAlive=False
    # raise Exception(msg)
    #raise SystemExit(msg)
    #raise Exception('exitState:' + resMsg)
    #exit(0)


class exitState(State):
    idleTime = 15.0

    def __init__(self, resMsg, phoneNum=None):
        logger.debug('exitState: %s', resMsg)
        commonExit(resMsg, phoneNum)

    def press1(self,  *unused):
        pass
    def press2(self,  *unused):
        pass


class confirmState(State):
    idleTime = 15.0

    def __init__(self,bookDate):
        self.bookDate = bookDate
        self.stateMessage = f'''You have selected {bookDate}
        Confirm State\n1-To Confirm\n2-To Reselect
        '''
        self.audioList = [key2file('confirmState1')] + date2audioFiles(bookDate,includeYear=True,includeDayOfWeek=True) + [key2file('confirmState2')] 
        self.speak()

    def press1(self, atm):
        # Save to DB, SMS to user
        tokenNum = storeBooking(atm.phoneNum, self.bookDate)
        self.audioList = [key2file('booked')]
        self.speak()
        resStr = 'Appointment confirmed!! \nDate - ' + self.bookDate + ' , \nToken number - ' + tokenNum + ' \n-Mayuri Hospital'
        atm.state = exitState(resStr,atm.phoneNum)

    def press2(self, atm):
        atm.state = bookState()

    def press9(self,atm):
        atm.state = talkState(atm.phoneNum)


class alreadyState(State):
    idleTime = 20.0

    def __init__(self, bookDate):
        self.existingBookingDate = bookDate
        self.stateMessage = 'You are already Registered\n1-To Update\n2-To Cancel'
        self.audioList = [key2file('alreadyState1')] + date2audioFiles(self.existingBookingDate,includeYear=True,includeDayOfWeek=True) + [key2file('alreadyState2')]
        self.speak()

    def press1(self, atm):
        atm.state = bookState()

    def press2(self, atm):
        cancelBooking(atm.phoneNum)
        self.audioList = [key2file('cancelled')]
        self.speak()
        resStr = 'Aapka ' + self.existingBookingDate + ' ka appointment cancel hogaya hai \n- Mayuri Hospital'
        atm.state = exitState(resStr,atm.phoneNum)

    def press9(self, atm):
        atm.state = talkState(atm.phoneNum)

@singleton
class ATM:
    def __init__(self,phoneNum='9876543210'):
        if not re.search(r"^\d{10}$", phoneNum):
            raise Exception('not a 10 digit number - ' + phoneNum)
        self.phoneNum = phoneNum        
        

    def reset(self,phoneNum):
        if not re.search(r"^\d{10}$", phoneNum):
            raise Exception('not a 10 digit number - ' + phoneNum)
        
        self.phoneNum = phoneNum
        bookDate = isNumRegistered(phoneNum)
        if not bookDate:
            self.state = welcomeState()
        else:
            self.state = alreadyState(bookDate)

    def press(self,selNum):
        if not isinstance(selNum,str):
            logger.error('invalid Number - Not a string')
            return

        if len(selNum) != 1:
            logger.error('invalid selection - should be single char')
            return 
        
        if selNum not in '0123456789#*':
            logger.error('invalid selection - Not a allowed char')
            return

        if selNum == '*':
            selNum = 'Star'   
        elif selNum == '#':
            selNum = 'Hash'

        logger.debug('recvd - %s',selNum)
         
        funName = "press" + str(selNum) 
        if self and self.state:
            class_method = getattr(self.state,funName) 
            result = class_method(self)

def remindToPress(atmObj):
    logger.debug(threading.current_thread())
    startNonBlockingProcess([key2file('retry')],True)
    if atmObj:
        timer3 = threading.Timer(2.0, atmObj.state.speak)
        timer3.start()
    else:
        logger.critical('atmObj is None')

def noResponseExit():
    startNonBlockingProcess([key2file('timeout')],True)
    logger.debug('reached in noResponseExit')
    commonExit('no response exit',None)
    #os.kill(os.getpid(), signal.SIGTERM)


timer1, timer2 = None, None

def stop_Timer():
    logger.debug('inside Stop Timer')
    global timer1
    global timer2

    if timer1:
        timer1.cancel()
        timer1 = None
    
    if timer2:
        timer2.cancel()
        timer2 = None

def init_Timer(idleTime,atmObj):
    # traceback.print_stack()
    global timer1
    global timer2
    logger.debug(' --- init_Timer ---')
        
    timer1 = threading.Timer(idleTime + 10.0, remindToPress,[atmObj])
    timer1.setName('remindToPress')
    timer1.start()

    timer2 = threading.Timer(idleTime + 40.0, noResponseExit)
    timer1.setName('noResponseExit')
    timer2.start()

# def keyPressCallback(channel,atmObj):
#     stop_Timer()
#     keyPressed = read_dtmf()
#     if not keyPressed:    
#         return

#     print('key pressed - %s',str(keyPressed))
#     if atmObj:
#         atmObj.press(keyPressed)
#     else:
#         logger.critical('invalid atmObj')
#     init_Timer(atmObj.state.idleTime,atmObj)

def keyPressCallback2(keyPressed,atmObj):
    global atm

    stop_Timer()
    if not keyPressed:
        return
    logger.debug('key pressed - %s' % (str(keyPressed)))
    if atmObj:
        atmObj.press(keyPressed)
    else:
        logger.critical('invalid atmObj')

    if atm: # this is required for the case when keypress result in exitState
        stop_Timer()
        init_Timer(atmObj.state.idleTime,atmObj)

def answerCall(callerId):
    logger.debug('in answering callerId is')
    phoneNum = callerId[-10:]
    global atm
    #print(phoneNum)
    while atm != None:
        logger.critical('waiting for the last call to finish')
        time.sleep(1)

    atm = ATM(phoneNum)
    atm.reset(phoneNum)

    init_Timer(atm.state.idleTime,atm)
    
    # callback_rt = lambda x,atmObj=atm:keyPressCallback(x,atmObj)
    # register_callback(callback_rt)
    callback_rt = lambda x,atmObj=atm:keyPressCallback2(x,atmObj)
    sim800l.callback_dtmf(callback_rt)
    
    logger.debug('answering call - %s',str(callerId))
    sim800l.answer_call()

def cleanupAfterCallEnd() -> None:
    global atm
    if atm == None:
        logger.critical('call already ended')
        return

    logger.debug('Call Ended')
    sim800l.callback_dtmf_clear()
    # remove_callback()
    logger.debug('destroying all')
    stopNonBlockingProcess()
    stop_Timer()
    # gpio_clean()

    del atm
    atm = None

def main4():
    
    # LOG_FILENAME='logging.conf'
    LOG_FILENAME='prod.log'
    # https://docs.python.org/3/library/logger.html#logrecord-attributes
    # logging.basicConfig(filename=LOG_FILENAME, format='%(asctime)s:%(levelname)s:%(filename)s:%(funcName)s:%(lineno)d >>> %(message)s', level=logging.DEBUG)
    # Add the log message handler to the logger
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(filename)s:%(funcName)s:%(lineno)d >>> %(message)s')
    handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=1024*1024*50, backupCount=2) #50MB
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    # logger.propagate = False
    # logger.fileConfig('./logging.conf')

    try:
	
        print('initializing now')
        gpio_initialize()
        gsm_power_on()
        time.sleep(5)
        ret = sim800l.check_network()
        logger.debug('ret val of check_network: %s',str(ret))
        #time.sleep(10)
        #if not isNetworkReg():
            #send telegram message
            #wait and re-check

        sim800l.callback_incoming(answerCall)
        sim800l.callback_no_carrier(cleanupAfterCallEnd)
        
        while True:
            sim800l.check_incoming()
    
    except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
        print("Keyboard interrupt")
    except Exception as E:
        print(E)
    finally:
        gpio_clean()

main4()
