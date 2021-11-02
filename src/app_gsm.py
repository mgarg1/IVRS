import abc
import os
from dataAccess import findNextDates, isNumRegistered, storeBooking, cancelBooking
from dateToNum import date2audioFiles, startNonBlockingProcess, stopNonBlockingProcess, key2file, key2fileWithoutMap, waitForJoin
from phoneCmds import registerCallback
from dtmf_decoder3 import read_dtmf, register_callback, remove_callback, gpio_initialize, gpio_clean, gsm_rst, gsm_power_on
from singleton_decorator import singleton
import re
from threading import Timer
# from multiprocessing import shared_memory
from sim800l import SIM800L

import logging
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
    
    if phoneNum:
        sim800l.send_sms(phoneNum,msg)
    checkEndCall()
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
        commonExit('exitState:' + resMsg, phoneNum)

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
        funName = 'self.state.press' + str(selNum) + '(self)'
        eval(funName)


# async def main2():
#    atm = ATM()
#    while(1):
#        timer = Timer(2, timeout_callback)
#        inRes = input()
#        funName = atm.press(int(inRes))

# if __name__ == '__main__':
#     asyncio.run(main2())

def remindToPress(atmObj):
    startNonBlockingProcess([key2file('retry')],True)
    timer3 = Timer(2.0, atmObj.state.speak)
    timer3.start()

def noResponseExit():
    startNonBlockingProcess([key2file('timeout')],True)
    logger.debug('reached in noResponseExit')
    commonExit('no response exit',None)
    #os.kill(os.getpid(), signal.SIGTERM)


timer1, timer2 = None, None

def stop_Timer():
    global timer1
    global timer2
    if timer1:
        timer1.cancel()
    if timer2:
        timer2.cancel()

def init_Timer(idleTime,atmObj):
    global timer1
    global timer2

    stop_Timer()
        
    timer1 = Timer(idleTime + 10.0, remindToPress,[atmObj])
    timer1.start()

    timer2 = Timer(idleTime + 40.0, noResponseExit)
    timer2.start()
    

def destroyAll():
    stopNonBlockingProcess()
    stop_Timer()
    # gpio_clean()

def keyPressCallback(channel,atmObj):
    stop_Timer()
    keyPressed = read_dtmf()
    if not keyPressed:    
        return

    logger.debug('key pressed - %s',str(keyPressed))
    if atmObj:
        atmObj.press(keyPressed)
    else:
        logger.critical('invalid atmObj')
    init_Timer(atmObj.state.idleTime,atmObj)

# def main4(phoneNum):
#     #sys.stdout.flush()
#     # destroyAll()
#     global keepAlive
#     keepAlive = True
#     # gpio_initialize()
#     atm = ATM(phoneNum)
#     atm.reset(phoneNum)

#     init_Timer(atm.state.idleTime,atm)
    
#     callback_rt = lambda x,atmObj=atm:keyPressCallback(x,atmObj)
#     register_callback(callback_rt)

#      # Attach to an existing shared memory block
#     shm_b = shared_memory.SharedMemory(SHM_NAME)
#     buf1 = shm_b.buf
#     logger.debug('buffer value---->  ' + str(int(buf1[0])))

#     while keepAlive and appCtx['keepAlive'] and int(buf1[0])==255:
#         pass
    
#     if(int(buf1[0])!=255):
#         stopNonBlockingProcess()
#         buf1[0] = 255

#     shm_b.close()
#     remove_callback()
#     logger.debug('Main Process ended')
#     destroyAll()
#     del atm
#     atm = None
#     global retVal
#     logger.debug('\nMain EXITED\n')
#     return retVal

def answerCall(callerId):
    #print('callerId is')
    phoneNum = callerId[-10:]
    global atm
    #print(phoneNum)
    atm = ATM(phoneNum)
    atm.reset(phoneNum)

    init_Timer(atm.state.idleTime,atm)
    
    callback_rt = lambda x,atmObj=atm:keyPressCallback(x,atmObj)
    register_callback(callback_rt)

    print('answering call')
    print(callerId)

    sim800l.answer_call()

def cleanCall():
    pass

def checkEndCall():
    global atm
    print('Call Ended')
    remove_callback()
    destroyAll()
    del atm
    atm = None
    print('Ending call now')
    sim800l.end_call()

def resetGSMHAT():
    gsm_power_on()

def main4():
    gpio_initialize()
    resetGSMHAT()
    #time.sleep(10)
    #if not isNetworkReg():
        #send telegram message
        #wait and re-check

    sim800l.callback_incoming(answerCall)
    sim800l.callback_no_carrier(checkEndCall)
    
    while True:
        sim800l.check_incoming()

    gpio_clean()

main4()

# def preMain():
#     if len(sys.argv) != 2:
#         logger.debug('invalid argument list')
#     else:
#         phoneNum=str(sys.argv[1])
#         logger.debug('phone num recvd -> ' + phoneNum)
#         logger.debug('pid - ' + str(os.getpid()))
#         main3(phoneNum)
