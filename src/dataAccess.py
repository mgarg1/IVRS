from datetime import datetime,timedelta
from tinydb import TinyDB, Query,where
import constants

phoneDB = TinyDB(constants.PHONE_DB_FILE)

def isNumRegistered(phoneNum):
    records = phoneDB.search(where('phoneNum') == phoneNum)
    if len(records) > 0:
        return records[0]['bookDate']
    else:
        return False

def findNextDates(numOfDays=5,today=datetime.now()):
    days = []
    currDelta = 1
    holiday_list = open(constants.HOLIDAY_DB_FILE).readlines()
    holiday_list = [i.strip() for i in holiday_list]
    print(holiday_list)

    while len(days) < numOfDays:
        thisDay = today+timedelta(days=currDelta)
        thisDay_str = thisDay.strftime(constants.DATE_FORMAT)
        
        # This day is NOT thursday AND This day is not a holiday AND Num of Apts is less than constants.BOOK_LIMIT 
        if thisDay.weekday() != 3 and thisDay_str not in holiday_list and totalBookOnDate(thisDay_str) < constants.BOOK_LIMIT:
            days.append(thisDay_str)
        
        currDelta += 1
    return days

def totalBookOnDate(bookDate):
    #phoneData = Query()
    return phoneDB.count(where('bookDate') == bookDate)

def allAptsOnDate(bookDate,obfuscate=True):
    #phoneData = Query()
    totalBookings = phoneDB.search(where('bookDate') == bookDate)
    booking_data = 'date: ' + bookDate + '\n'
    totalBookings_sorted = sorted(totalBookings, key=lambda k: int(k['tokenNum'])) 
    for i in totalBookings:
        if obfuscate:
            booking_data += '%s. ####%s' % (i['tokenNum'],i['phoneNum'][-6:])
        else:
            booking_data += '%s. %s' % (i['tokenNum'],i['phoneNum'])
        booking_data += "\n"

    return booking_data

def storeBooking(phoneNum,bookDate):
    thisToken = phoneDB.search(where('tokenDate') == bookDate)
    print(thisToken)
    maxToken = 1
    if thisToken:
        maxToken = int(thisToken[0]['maxTokenNum']) + 2
    #update the maxToken Entry
    phoneDB.upsert({'tokenDate': bookDate, 'maxTokenNum': str(maxToken)}, where('tokenDate') == bookDate)
    # insert the new appointment
    phoneDB.insert({'phoneNum': phoneNum, 'bookDate': bookDate, 'tokenNum': str(maxToken)})
    return str(maxToken)

def cancelBooking(phoneNum):
    phoneDB.remove(where('phoneNum') == phoneNum)

def removeStaleBooking(staleDate):
    phoneDB.remove(where('bookDate') == staleDate)
    phoneDB.remove(where('tokenDate') == staleDate)


def addHoliday(newDate):
    # thisDay.strftime("%d-%B-%Y")
    # Always use date in this format 22-12-2012, 02-01-2012 
    with open(constants.HOLIDAY_DB_FILE, 'a') as file:
        file.write(newDate)


#aa = findNextDates()
#for x in aa:
#    print(x)
