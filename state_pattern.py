import abc
from dataAccess import checkIfReg,findNextDates

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

class welcomeState(State):
    def __init__(self):
        self.stateMessage = 'welcome to IVRS: \n1-To Book\n2-To Talk\n'
        # print('welcome to IVRS: \n1-To Book\n2-To Talk\n')
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
            self.stateMessage = self.stateMessage + 'Press ' +str(x+1)+' for '+self.availDates[x])
        self.speak()

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
        self.checkKeyPress(6)
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
        self. 'You have selected ' + bookDate)
        print('Confirm State\n1-To Confirm\n2-To Reselect')

    def press1(self, atm):
        print('Booked')
        # Save to DB, SMS to user
        exit()

    def press2(self, atm):
        atm.state = bookState()

class alreadyState(State):
    def __init__(self):
        print('You are already Registered\n1-To Update\n2-To Cancel')

    def press1(self,atm):
        atm.state = bookState()

    def press2(self,atm):
        exit()

    def press9(self,atm):
        atm.state = talkState()

class ATM:
    def __init__(self,isReg=False):
        if isReg:
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

    #   atm.press2() # default state is no card error no card
    #   atm.press1() # ok state is has card
    #   atm.press1() # error  card already in
    #   atm.press2() # ok  state become no card
    #   atm.press2() # error no card
    #


#if __name__ == "__main__":
#    while(1):
#        inRes = input()
#        if inRes == '1':
#            print('pressed 1')
#        elif inRes == '2':
#            print('pressed 2')
#        else:
#            print('invalid choice')
#    
