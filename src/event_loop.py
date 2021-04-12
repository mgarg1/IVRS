# https://stackoverflow.com/a/59203700/1496826

import schedule
import time
import datetime
import constants
import sensitive

# from dataAccess import removeStaleBooking,allAptsOnDate,addHoliday
from ivrs_utils import sendMessageToTelegram,getUpdatesFromTelegram

def removeOldBooking():
    todaysDate = datetime.datetime.now().strftime(constants.DATE_FORMAT)
    removeStaleBooking(todaysDate)

def removeOldHolidays():
    #TODO#
    pass

def postDailyAptList():
    todaysDate = datetime.datetime.now().strftime(constants.DATE_FORMAT)
    apt_data_text = allAptsOnDate(todaysDate)
    if apt_data_text and apt_data_text != '':
        r = sendMessageToTelegram(apt_data_text,sensitive.TELEGRAM_GROUP_CHATID,'false')

def readTelegramRequests():
    reqs = getUpdatesFromTelegram()
    reqs = reqs.json()['result']

    for req in reqs:
        sender=None
        text_msg=None
        try:
            if req['message']['entities']['type'] == 'bot_command':
                sender = req['message']['from']['id']
                text_msg = req['message']['text']

        except KeyError:
            continue
        
        # access list
        if sender in [sensitive.TELEGRAM_MOHIT_CHATID]:
            date_args=None
            text_msg_split=text_msg.split()
            if len(text_msg_split) == 1:
                date_args=None
            elif len(text_msg_split) == 2:
                date_args=text_msg_split[1]
            else:
                continue

            if date_args:
                try:
                    datetime.datetime.strptime(date_args, constants.DATE_FORMAT)
                except ValueError:
                    sendMessageToTelegram('invalid date format, should be DD-Month-YYYY',sender,'false')

            if 'pub' in text_msg:
                if not date_args:
                    date_args = datetime.datetime.now().strftime(constants.DATE_FORMAT)
                
                apt_data_text = allAptsOnDate(date_args)
                if apt_data_text and apt_data_text != '':
                    r = sendMessageToTelegram(apt_data_text,sender,'false')

            # elif 'rem' in text_msg:
            #     removeStaleBooking(date_args)
            #     r = sendMessageToTelegram(apt_data_text,sender,'false')

            elif 'hol' in text_msg:
                if date_args:
                    apt_data_text = allAptsOnDate(date_args)
                    addHoliday(date_args)
                    r = sendMessageToTelegram('holiday added successfully, pls inform these apts : \n ' + str(apt_data_text),sender,'false')
                else:    
                    r = sendMessageToTelegram('date must for hol, should be in DD-Month-YYYY,sender,'false')

# schedule.every().hour.do(job)
# schedule.every(5).to(10).minutes.do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
# schedule.every().minute.at(":17").do(job)


def main():

    schedule.every().day.at("09:00").do(postDailyAptList)
    schedule.every().day.at("23:30").do(removeOldBooking)
    schedule.every().day.at("23:35").do(removeOldHolidays)
    # schedule.every(1).minutes.do(readTelegramRequests)

    while True:
        schedule.run_pending()
        time.sleep(1)

main()