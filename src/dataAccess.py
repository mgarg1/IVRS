from datetime import datetime, timedelta
from tinydb import TinyDB, where
import constants
import logging

logger = logging.getLogger('rootLogger')

phoneDB = TinyDB(constants.PHONE_DB_FILE)
archiveDB = TinyDB(constants.ARCHIVE_DB_FILE)

def isNumRegistered(phoneNum):
    records = phoneDB.search(where('phoneNum') == phoneNum)
    if len(records) > 0:
        return records[0]['bookDate']
    
    return False


def findNextDates(numOfDays=5,startDate=None):
    currDelta = 0 # Accept today's reservation
    holiday_list = open(constants.HOLIDAY_DB_FILE).readlines()
    holiday_list = [i.strip() for i in holiday_list]
    logger.debug('holiday list - %s',str(holiday_list))

    if not startDate:
        startDate = datetime.now()
        if startDate.hour > 9: # If calling after 11 am then you will get tomorrow's number
            currDelta = 1

    days = []
    while len(days) < numOfDays:
        thisDay = startDate+timedelta(days=currDelta)
        thisDay_str = thisDay.strftime(constants.DATE_FORMAT)
        
        # This day is NOT thursday AND This day is not a holiday AND Num of Apts is less than constants.BOOK_LIMIT 
        if thisDay.weekday() != 3 and thisDay_str not in holiday_list and totalBookOnDate(thisDay_str) < constants.BOOK_LIMIT:
            days.append(thisDay_str)
        
        currDelta += 1
    return days

def totalBookOnDate(bookDate):
    #phoneData = Query()
    return phoneDB.count(where('bookDate') == bookDate)

def allAptsOnDate(bookDate,obfuscate=True) -> str:
    #phoneData = Query()
    totalBookings = phoneDB.search(where('bookDate') == bookDate)
    booking_data = 'date: ' + bookDate + '\n'
    totalBookings_sorted = sorted(totalBookings, key=lambda k: int(k['tokenNum'])) 
    for i in totalBookings_sorted:
        if obfuscate:
            booking_data += '%s. ####%s' % (i['tokenNum'],i['phoneNum'][-6:])
        else:
            booking_data += '%s. %s' % (i['tokenNum'],i['phoneNum'])
        booking_data += "\n"

    return booking_data

def storeBooking(phoneNum,bookDate):
    # oldBookDate = isNumRegistered(phoneNum)
    # check if the phone number is registered on the same date
    records = phoneDB.search(where('phoneNum') == phoneNum)
    if len(records) > 0 and records[0]['bookDate'] == bookDate:
        return records[0]['tokenNum']

    thisToken = phoneDB.search(where('tokenDate') == bookDate)
    # print(thisToken)
    newToken = None
    if thisToken:
        maxToken = int(thisToken[0]['maxTokenNum'])
        # if maxToken > 39:
        newToken = maxToken + 1
        # else:
        #     newToken = maxToken + 2
    else:
        newToken = constants.START_TOKEN_NUM
    #update the maxToken Entry
    phoneDB.upsert({'tokenDate': bookDate, 'maxTokenNum': str(newToken)}, where('tokenDate') == bookDate)
    # insert the new appointment
    phoneDB.upsert({'phoneNum': phoneNum, 'bookDate': bookDate, 'tokenNum': str(newToken)}, where('phoneNum') == phoneNum)
    return str(newToken)

def cancelBooking(phoneNum):
    phoneDB.remove(where('phoneNum') == phoneNum)

def removeStaleBooking(staleDate):
    apt_data_text = allAptsOnDate(staleDate, False)
    archiveDB.insert({staleDate : str(apt_data_text)})
    
    phoneDB.remove(where('bookDate') == staleDate)
    phoneDB.remove(where('tokenDate') == staleDate)

def listHolidays() -> str:
    fileContents = ''
    with open(constants.HOLIDAY_DB_FILE, 'r') as file:
        fileContents = file.read()
    return fileContents

def clearHolidaysList() -> None:
    with open(constants.HOLIDAY_DB_FILE, 'a') as file:
        file.truncate(0)

def addHoliday(newDate:str) -> None:
    # thisDay_str = thisDay.strftime(constants.DATE_FORMAT)
    # thisDay.strftime("%d-%B-%Y")
    # Always use date in this format 22-12-2012, 02-01-2012 
    with open(constants.HOLIDAY_DB_FILE, 'a') as file:
        file.write("\n")
        file.write(newDate)


#aa = findNextDates()
#for x in aa:
#    print(x)
