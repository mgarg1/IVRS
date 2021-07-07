# https://stackoverflow.com/a/59203700/1496826

import schedule
import time
import datetime
import constants
import sensitive

# we need this sensitive information in sensitive file
# PASTEBIN_API_KEY
# TELEGRAM_AUTH_TOKEN
# TELEGRAM_BOT_ID
# TELEGRAM_MOHIT_CHATID
# TELEGRAM_AJAY_CHATID
# TELEGRAM_GROUP_CHATID

from dataAccess import removeStaleBooking,allAptsOnDate,addHoliday
from ivrs_utils import sendMessageToTelegram,getUpdatesFromTelegram,checkIfSenderIsAllowed

def removeOldBooking():
    todaysDate = datetime.datetime.now().strftime(constants.DATE_FORMAT)
    removeStaleBooking(todaysDate)

def removeOldHolidays():
    #TODO#
    pass

def postDailyAptList():
    pubCmd(sensitive.TELEGRAM_GROUP_CHATID, None)

def convertReqs(msgs):
    parsedLists = []
    for req in msgs:
        try:
            # if req['message']['entities'][0]['type'] == 'bot_command':
            sender = req['message']['from']['id']
            text_msg = req['message']['text']
            update_id = req['update_id']
        except KeyError:
            continue

        parsedLists.append({'sender': sender, 'msg': text_msg, 'update_id': update_id})

    return parsedLists


def checkValidDate(date_str):
    try:
        datetime.datetime.strptime(date_str, constants.DATE_FORMAT)
    except (ValueError, TypeError):
        return False
    else:
        return True


# sendMessageToTelegram('invalid date format, should be DD-Month-YYYY',sender,'false')
def pubCmd(senderId, date_arg):
    if not checkValidDate(date_arg):
        date_arg = datetime.datetime.now().strftime(constants.DATE_FORMAT)

    apt_data_text = allAptsOnDate(date_arg)
    if apt_data_text:
        r = sendMessageToTelegram(apt_data_text,senderId,'false')
    return r

def holCmd(senderId, date_arg):
    apt_data_text = ''
    if checkValidDate(date_arg):
        apt_data_text = allAptsOnDate(date_arg,False)
        addHoliday(date_arg)

        if apt_data_text:
            apt_data_text = 'holiday added successfully, pls inform these apts:\n' + apt_data_text

        r = sendMessageToTelegram(apt_data_text,senderId,'false')
    else:
        r = sendMessageToTelegram('date must for hol, should be in DD-Month-YYYY',senderId,'false')
    return r


LAST_UPDATE_ID = None

def readTelegramRequests():
    global LAST_UPDATE_ID
    reqs = getUpdatesFromTelegram(offset=LAST_UPDATE_ID)
    reqs = reqs.json()['result']
    # "update_id":981483207,    

    for req in convertReqs(reqs):
        # access list
        print('serving reqs')
        if not checkIfSenderIsAllowed(req['sender']):
            return

        text_msg_split=req['msg'].split()
        cmdTxt = ''
        if text_msg_split:
            cmdTxt = text_msg_split[0]

        r = None
        arg1 = None if len(text_msg_split) < 2 else text_msg_split[1]
        # arg2 = None if len(text_msg_split) < 3 else text_msg_split[2]

        if cmdTxt == '/pub':
            r = pubCmd(sensitive.TELEGRAM_GROUP_CHATID, arg1)
        elif cmdTxt == '/hol':
            r = holCmd(req['sender'], arg1)

        if r.status_code != 200:
            print('request response isnt success\n')


        print('UPDATING UPDATE_ID\n\n')
        LAST_UPDATE_ID = req['update_id'] + 1

        # elif 'rem' in text_msg:
        #   removeStaleBooking(date_args)
        #   r = sendMessageToTelegram(apt_data_text,sender,'false')


# schedule.every().hour.do(job)
# schedule.every(5).to(10).minutes.do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
# schedule.every().minute.at(":17").do(job)


def main():

    schedule.every(5).minutes.do(readTelegramRequests)
    schedule.every().day.at("09:00").do(postDailyAptList)
    schedule.every().day.at("23:30").do(removeOldBooking)
    schedule.every().day.at("23:35").do(removeOldHolidays)

    while True:
        schedule.run_pending()
        time.sleep(1)


main()
