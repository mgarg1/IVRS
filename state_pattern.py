import abc
from dataAccess import findNextDates,isNumRegistered,storeBooking

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
        self.wrongInput(atm)

    def press0(self, atm):
        self.wrongInput(atm)

    def wrongInput(self, atm):
        print('You have entered a wrong option. Please retry\n')
        atm.state.speak()
        # raise NotImplementedError('')

    def speak(self):
        print(self.stateMessage)
        map(playWord,self.audioList)
        #playAudioList(self.audioList)

class welcomeState(State):
    def __init__(self):
        self.stateMessage = 'welcome to IVRS: \n1-To Book\n2-To Talk\n'
        # print('welcome to IVRS: \n1-To Book\n2-To Talk\n')
        self.audioList = ['welcomeStateMsg.wav']
        self.speak()

    def press1(self, atm):
        atm.state  = bookState()

    def press2(self, atm):
        atm.state = talkState()
    

class bookState(State):
    def __init__(self):
        self.availDates = findNextDates(numOfDays=8)
        #print('Booking State\n 1-Today\n2-Tomorrow\n3-DayAfter')
        self.stateMessage = 'Booking State:\n'
        for x in range(0,len(self.availDates)):
            self.stateMessage += f'Press {str(x+1)} for {self.availDates[x]} \n'
            self.audioList += self.createAudioList(str(x+1),self.availDates[x])
        self.speak()


    def createAudioList(keyNum,availDate):
        return ['press.wav'] + num2audio(str(x+1)) + ['for.wav'] + date2audio(availDate)
        #return date2audio(availDate) + ['keliye.wav'] + num2audio(str(x+1) + ['dabayein.wav']
        
    def checkKeyPress(self,numPressed):
        atm.state = confirmState(self.availDates[numPressed-1])
    
    def press1(self, atm):
        self.checkKeyPress(1)
    def press2(self, atm):
        self.checkKeyPress(2)
    def press3(self, atm):
        self.checkKeyPress(3)
    def press4(self, atm):
        self.checkKeyPress(4)
    def press5(self, atm):
        self.checkKeyPress(5)
    def press6(self, atm):
        self.checkKeyPress(6):
    def press7(self, atm):
        self.checkKeyPress(7)
    def press8(self, atm):
        self.checkKeyPress(8)

    def press9(self, atm):
        #self.checkKeyPress(9)
        pass

class confirmState(State):
    def __init__(self,bookDate):
        self.bookDate = bookDate
        self.stateMessage = f'''You have selected {bookDate}
        Confirm State\n1-To Confirm\n2-To Reselect
        '''
        self.audioList = ['confirmStateSelMsg.wav'] + date2audioFiles(bookDate) + ['confirmStateConMsg.wav'] 
        self.speak()

    def press1(self, atm):
        print('Booked')
        # Save to DB, SMS to user
        storeBooking(atm.phoneNum, self.bookDate)
        exit()

    def press2(self, atm):
        atm.state = bookState()

class alreadyState(State):
    def __init__(self):
        self.stateMessage = 'You are already Registered\n1-To Update\n2-To Cancel'
        self.audioList = ['alreadyStateMsg.wav']
        self.speak()

    def press1(self,atm):
        atm.state = bookState()

    def press2(self,atm):
        exit()

    def press9(self,atm):
        atm.state = talkState()

class ATM:
    def __init__(self,phoneNum='9876543210'):
        self.phoneNum = phoneNum
        if isNumRegistered(phoneNum):
            self.state = alreadyState()
        else:
            self.state = welcomeState()

    def press(self,selNum):
        funName = 'self.state.press' + str(selNum) + '(self)'
        result = eval(funName)

if __name__ == "__main__":
   atm = ATM()
   while(1):
       inRes = input()
       funName = atm.press(int(inRes))

