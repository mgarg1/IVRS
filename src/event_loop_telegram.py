#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

# https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/conversationbot.py
"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import re
import sensitive
import constants
import datetime
import json
import pytz
import subprocess

from dataAccess import findNextDates,storeBooking,allAptsOnDate

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

ENTER_PHONE_NUM, CONFIRM_DATE, CONFIRMATION, SEL_DATE  = range(4)
APP_GSM_LOC = '/home/pi/Desktop/IVRS/app_runner.sh'

def start(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks the user about their gender."""
    
    phoneNum = None
    msgs = update.message.text.split()
    
    if len(msgs) > 1 and re.match(r"^[0-9]{10}$", msgs[1]):
        phoneNum = msgs[1]
        # context.user_data["key"] = querydata
        context.chat_data["mg_data"] = {'phone_num':phoneNum}

    if not phoneNum:
        update.message.reply_text(
            'Enter correct 10-digit phone number without 0\n'
            'Send /cancel to stop. \n\n'
        )

        return ENTER_PHONE_NUM

    return SEL_DATE

def enter_phone_num(update: Update, context: CallbackContext) -> int:
    msg = update.message.text
    print('found-->' + msg)
    if re.match(r"^[0-9]{10}$", msg):
        # context.user_data["key"] = querydata
        context.chat_data["mg_data"] = {'phone_num':msg}
        
        dates = findNextDates()
        reply_keyboard = [ [individualArray] for individualArray in dates]
        # reply_keyboard = [dates]
        phoneNum = context.chat_data['mg_data']['phone_num']
        update.message.reply_text(
            'Booking process started for {} \n Choose available dates \n Send /cancel to stop. \n\n'.format(phoneNum),
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, input_field_placeholder='Choose a date?'
            ),
        )
        
        return CONFIRM_DATE
    else:
        update.message.reply_text(
            'Enter correct 10-digit phone number without 0'
            'Send /cancel to stop. \n\n'
        )

        return ENTER_PHONE_NUM


def selectDate(update: Update, context: CallbackContext) -> int:
    """Stores the selected gender and asks for a photo."""
    dates = findNextDates()
    reply_keyboard = [ [individualArray] for individualArray in dates]
    # reply_keyboard = [dates]
    phoneNum = context.chat_data['mg_data']['phone_num']
    update.message.reply_text(
        'Booking process started for {} \n Choose available dates \n Send /cancel to stop. \n\n'.format(phoneNum),
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Choose a date?'
        ),
    )

    return CONFIRM_DATE

def confirm_date(update: Update, context: CallbackContext):
    reply_keyboard = [['YES', 'NO']]
    selectedDate = update.message.text
    context.chat_data['mg_data']['selected_date'] = selectedDate
    print(context.chat_data["mg_data"])
    update.message.reply_text(
        'You selected {} \n Click on Yes to Confirm \n Send /cancel to stop. \n\n'.format(selectedDate),
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Confirm Yes/NO?'
        ),
    )
    return CONFIRMATION

def book_appointment(update: Update, context: CallbackContext):
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


# def checkValidDate(date_str):
#     try:
#         datetime.datetime.strptime(date_str, constants.DATE_FORMAT)
#     except (ValueError, TypeError):
#         return False
#     else:
#         return True


# # sendMessageToTelegram('invalid date format, should be DD-Month-YYYY',sender,'false')
# def pubCmd(senderId, date_arg):
#     # if not checkValidDate(date_arg):
#     date_arg = datetime.datetime.now().strftime(constants.DATE_FORMAT)

    
#     if apt_data_text:
#         r = sendMessageToTelegram(apt_data_text,senderId,'false')
#     return r


def pubCmd(update: Update, context: CallbackContext) -> None:
    if update:
        print(update.message.text)

    date_arg = datetime.datetime.now().strftime(constants.DATE_FORMAT)
    apt_data_text = allAptsOnDate(date_arg,False)
    context.bot.send_message(chat_id=sensitive.TELEGRAM_GROUP_CHATID, text=apt_data_text)

def restartCmd(update: Update, context: CallbackContext) -> None:
    subprocess.check_output([APP_GSM_LOC],shell=False)    
    context.bot.send_message(chat_id=sensitive.TELEGRAM_GROUP_CHATID, text='app restarted')

def pubCmd2(context: CallbackContext) -> None:
    pubCmd(None,context)

def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    token22 = sensitive.TELEGRAM_BOT_ID + ':' + sensitive.TELEGRAM_AUTH_TOKEN
    updater = Updater(token=token22)

    # updater = Updater("TOKEN")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('book', start)],
        states={
            ENTER_PHONE_NUM: [MessageHandler(Filters.regex(r'^[0-9]{10}$'), enter_phone_num)],
            SEL_DATE:[MessageHandler(Filters.text, selectDate)],
            #TODO: regex for Date
            CONFIRM_DATE: [MessageHandler(Filters.text, confirm_date)],
            CONFIRMATION: [MessageHandler(Filters.regex('^(NO|YES)$'), book_appointment)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(CommandHandler("pub", pubCmd))
    dispatcher.add_handler(CommandHandler("restart", restartCmd))
    
    jobQueue = updater.job_queue

    # tz = pytz.timezone('Asia/Kolkata')
    # start_tz = datetime.now().astimezone(tz)
    # datetime.time(hour=3, minute=30, second=00).astimezone(tz)

    # print ("Time (RSA): %s" % start_tz.strftime("%d-%m-%Y %H:%M:%S"))

    jobQueue.run_daily(pubCmd2, days=(0, 1, 2, 3, 4, 5, 6), time=datetime.time(hour=3, minute=30, second=00))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
