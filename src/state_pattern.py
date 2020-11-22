import abc,os,signal
from dataAccess import findNextDates,isNumRegistered,storeBooking,cancelBooking
from dateToNum import date2audioFiles, startNonBlockingProcess,key2file,key2fileWithoutMap
from phoneCmds import registerCallback

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
        atm.state = talkState()
    
    def press9(self, atm):
        atm.state = talkState()

class talkState(State):
    def __init__(self):
        self.idleTime = 12.0
        self.stateMessage = 'Your callback is registered. You will get a callback soon'
        registerCallback(atm.phoneNum)
        self.audioList = [key2file('callback')]
        self.speak()
        exit()
    
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
        print('Booked')
        exit()

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
        print('cancelled')
        exit()

    def press9(self,atm):
        atm.state = talkState()

class ATM:
    def __init__(self,phoneNum='9876543210'):
        self.phoneNum = phoneNum
        bookDate = isNumRegistered(phoneNum)
        if bookDate == False:
            self.state = welcomeState()
        else:
            self.state = alreadyState(bookDate)

    def press(self,selNum):
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

def main3():
    atm = ATM()
    while(1):
        idleTime = atm.state.idleTime

        timer1 = Timer(idleTime + 10.0, remindToPress,[atm])
        timer1.start()

        timer2 = Timer(idleTime + 40.0, noResponseExit)
        timer2.start()

        inRes = input()
        timer1.cancel()
        timer2.cancel()
        
        funName = atm.press(int(inRes))

if __name__ == '__main__':
    main3()