import abc


class State(object,metaclass = abc.ABCMeta):
    @abc.abstractmethod
    def press1(self, atm):
        raise NotImplementedError('')
    
    @abc.abstractmethod
    def press2(self, atm):
        raise NotImplementedError('')


class welcomeState(State):
    def __init__(self):
        print('welcome to py State Machine: \n1-nextState\n2-exit\n')

    def press1(self, atm):
        atm.state  = HasCard()

    def press2(self, atm):
        exit()
        # print('Error : no card')
    

class HasCard(State):
    def __init__(self):
        print('HasCard')

    def press1(self, atm):
        print('ok')
        atm.state = welcomeState()
    
    def press2(self, atm):
        print('Error : card already present')


class ATM:
    def __init__(self):
        self.state = welcomeState()
    def press1(self):
        self.state.press1(self)
    def press2(self):
        self.state.press2(self)

# if __name__ == "__main__":
#     atm = ATM()
#     atm.press2() # default state is no card error no card
#     atm.press1() # ok state is has card
#     atm.press1() # error  card already in
#     atm.press2() # ok  state become no card
#     atm.press2() # error no card



if __name__ == "__main__":
    while(1):
        inRes = input()
        if inRes == '1':
            print('pressed 1')
        elif inRes == '2':
            print('pressed 2')
        else:
            print('invalid choice')
    