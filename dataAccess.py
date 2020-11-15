from datetime import datetime,timedelta
from tinydb import TinyDB, Query,where

phoneDB = TinyDB('phoneDB.json')

BOOK_LIMIT = 2

def isNumRegistered(phoneNum):
    records = phoneDB.search(where('phoneNum') == phoneNum)
    if len(records) > 0:
        return records[0]['bookDate']
    else:
        return False

def findNextDates(numOfDays=5,today=datetime.now()):
    days = []
    currDelta = 1
    while len(days) < numOfDays:
        thisDay = today+timedelta(days=currDelta)
        thisDay = thisDay.strftime("%d-%B-%Y")
        if totalBookOnDate(thisDay) < BOOK_LIMIT:
            days.append(thisDay)
        currDelta += 1
    return days

def totalBookOnDate(bookDate):
    #phoneData = Query()
    totalBookings = phoneDB.search(where('bookDate') == bookDate)
    return len(totalBookings)


def storeBooking(phoneNum,bookDate):
    phoneDB.insert({'phoneNum': phoneNum, 'bookDate': bookDate})


def removeStaleBooking(staleDate):
    phoneData = Query()
    phoneDB.remove(phoneData.bookDate == staleDate)

#aa = findNextDates()
#for x in aa:
#    print(x)
