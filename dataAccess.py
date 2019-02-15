from datetime import datetime,timedelta

def checkIfReg(phoneNum):
    return false

def findNextDates(numOfDays=5,today=datetime.now()):
    days = []
    for x in range(1,numOfDays+1):
        thisDay = today+timedelta(days=x)
        days.append(thisDay.strftime("%d-%B-%Y"))
    return days


#aa = findNextDates()
#for x in aa:
#    print(x)
