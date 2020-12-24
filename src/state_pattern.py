import abc,os,signal
from dataAccess import findNextDates,isNumRegistered,storeBooking,cancelBooking
from dateToNum import date2audioFiles, startNonBlockingProcess,key2file,key2fileWithoutMap
from phoneCmds import registerCallback
import re

# import asyncio
from threading import Timer

# class Timer:
    # def __init__(self, timeout, callback):
    #     self._timeout = timeout
    #     self._callback = callback
    #     self._task = asyncio.ensure_future(self._job())

    # async def _job(self):
    #     await asyncio.sleep(self._timeout)
    #     await self._callback()

    # def cancel(self):
    #     self._task.cancel()

# async def timeout_callback():
#     await asyncio.sleep(0.1)
#     print('echo! - timeout_callback called')

# def timeout_callback():
#     print('echo! - timeout_callback called')


class State(object,metaclass = abc.ABCMeta):
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
        atm.state = talkState()

    def press0(self, atm):
        self.wrongInput(atm)

    def wrongInput(self, atm):
        print('You have entered a wrong option. Please retry\n')
        atm.state.speak()
        # raise NotImplementedError('')

    def speak(self):
        print(self.stateMessage)
        #print(self.audioList)
        startNonBlockingProcess(self.audioList)
        
class welcomeState(State):
    def __init__(self):
        self.idleTime = 12.0
        self.stateMessage = 'welcome to IVRS: \n1-To Book\n2-To Talk\n'
        # print('welcome to IVRS: \n1-To Book\n2-To Talk\n')
        self.audioList = [key2file('welcomeState1')]
        self.speak()

    def press1(self, atm):
        atm.state  = bookState()

    def press2(self, atm):
        atm.state = talkState(atm.phoneNum)
    
    def press9(self, atm):
        atm.state = talkState(atm.phoneNum)

class talkState(State):
    def __init__(self,phoneNum):
        self.idleTime = 12.0
        self.stateMessage = 'Your callback is registered. You will get a callback soon'
        registerCallback(phoneNum)
        self.audioList = [key2file('callback')]
        self.speak()
        resMsg='Callback registered,' + phoneNum
        atm.state = exitState(resMsg)
    
    def press1(self, atm):
        pass
    
    def press2(self, atm):
        pass

class bookState(State):
    def __init__(self):
        self.idleTime = 50.0
        self.availDates = findNextDates(numOfDays=8)
        #print('Booking State\n 1-Today\n2-Tomorrow\n3-DayAfter')
        self.stateMessage = 'Booking State:\n'
        self.audioList = []
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
        atm.state = talkState()

class exitState(State):
    def __init__(self,resMsg):
        print('exitState:' + resMsg, flush=True)
        # can write to someplace
        exit(0)
    def press1(self, atm):
        pass
    def press2(self, atm):
        pass


class confirmState(State):
    def __init__(self,bookDate):
        self.idleTime = 15.0
        self.bookDate = bookDate
        self.stateMessage = f'''You have selected {bookDate}
        Confirm State\n1-To Confirm\n2-To Reselect
        '''
        self.audioList = [key2file('confirmState1')] + date2audioFiles(bookDate) + [key2file('confirmState2')] 
        self.speak()

    def press1(self, atm):
        # Save to DB, SMS to user
        storeBooking(atm.phoneNum, self.bookDate)
        # TODO:: tell the day also e.g- wednesday
        self.audioList = [key2file('booked')]
        self.speak()
        resStr = 'Booking Confirmed,' + atm.phoneNum + ',' + self.bookDate
        atm.state = exitState(resStr)

    def press2(self, atm):
        atm.state = bookState()

    def press9(self,atm):
        atm.state = talkState()

class alreadyState(State):
    def __init__(self,bookDate):
        self.idleTime = 20.0
        self.stateMessage = 'You are already Registered\n1-To Update\n2-To Cancel'
        self.existingBookingDate = bookDate
        self.audioList = [key2file('alreadyState1')] + date2audioFiles(self.existingBookingDate) + [key2file('alreadyState2')]
        self.speak()

    def press1(self,atm):
        atm.state = bookState()

    def press2(self,atm):
        cancelBooking(atm.phoneNum)
        self.audioList = [key2file('cancelled')]
        self.speak()
        resStr='Booking Cancelled,' + atm.phoneNum + ',' + self.existingBookingDate
        atm.state = exitState(resStr)

    def press9(self,atm):
        atm.state = talkState()

class ATM:
    def __init__(self,phoneNum='9876543210'):
        
        if not re.search("^\d{10}$", phoneNum):
            raise Exception('not a 10 digit number - ' + phoneNum)
        
        self.phoneNum = phoneNum
        bookDate = isNumRegistered(phoneNum)
        if bookDate == False:
            self.state = welcomeState()
        else:
            self.state = alreadyState(bookDate)

    def press(self,selNum):
        print('recvd ' + selNum)
        if not isinstance(selNum,str):
            print('invalid Number - Not a string')
        if len(selNum) != 1:
            print('invalid selection - should be single char')
        if not selNum in '0123456789#*':
            print('invalid selection - Not a allowed char')

        funName = 'self.state.press' + str(selNum) + '(self)'
        result = eval(funName)


# async def main2():
#    atm = ATM()
#    while(1):
#        timer = Timer(2, timeout_callback)
#        inRes = input()
#        funName = atm.press(int(inRes))

# if __name__ == '__main__':
#     asyncio.run(main2())

def remindToPress(atmObj):
    startNonBlockingProcess([key2file('retry')])
    timer3 = Timer(5.0, atmObj.state.speak)
    timer3.start()

def noResponseExit():
    startNonBlockingProcess([key2file('retry')])
    os.kill(os.getpid(), signal.SIGTERM)

import sys

FIFO='myfifo1'


def main3():
    
    if len(sys.argv) != 2:
        print('invalid argument list')
        return;

    phoneNum=str(sys.argv[1])
    print('phone num recvd -> ' + phoneNum)
    
    #with open(FIFO,'rt') as fifo:
     #   fifo.flush()
         
    atm = ATM(phoneNum)
    
    while True:
        idleTime = atm.state.idleTime

        timer1 = Timer(idleTime + 10.0, remindToPress,[atm])
        timer1.start()

        timer2 = Timer(idleTime + 40.0, noResponseExit)
        timer2.start()

        with open(FIFO,'rt') as fifo:
            fifo.flush()

        with open(FIFO,'rt') as fifo:
            #inRes = getInput()
            inRes = fifo.read()
            if len(inRes) == 0:
                print('invalid data')
                continue

        timer1.cancel()
        timer2.cancel()
        inRes = inRes.strip() 
        funName = atm.press(inRes)

if __name__ == '__main__':
    main3()
