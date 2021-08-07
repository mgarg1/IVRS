#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

# https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/conversationbot.py

import logging
import sensitive
import constants
import datetime

from dataAccess import findNextDates,storeBooking,allAptsOnDate
import bookConversation

from telegram import Update
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

def pubCmd(update: Update, context: CallbackContext) -> None:
    if update:
        print(update.message.text)

    date_arg = datetime.datetime.now().strftime(constants.DATE_FORMAT)
    apt_data_text = allAptsOnDate(date_arg,False)
    context.bot.send_message(chat_id=sensitive.TELEGRAM_GROUP_CHATID, text=apt_data_text)

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
        entry_points=[CommandHandler('book', bookConversation.start)],
        states={
            constants.ENTER_PHONE_NUM: [MessageHandler(Filters.contact, bookConversation.enter_phone_num)],
            #TODO: regex for Date
            constants.SEL_DATE:[MessageHandler(Filters.text & ~(Filters.command), bookConversation.selectDate)],
            constants.CONFIRM_DATE: [MessageHandler(Filters.regex('^(YES|NO)$'), bookConversation.confirmDate)],
            # constants.CONFIRMATION: [MessageHandler(~Filters.command,bookConversation.book_appointment)],
            # constants.CONFIRM_DATE: [MessageHandler(Filters.regex('^(YES)$'), bookConversation.book_appointment)],
            constants.ALREADY_REGISTERED: [MessageHandler(Filters.regex('^(MODIFY|DEREGISTER)$'), bookConversation.alreadyRegistered)]
        },
        fallbacks=[CommandHandler('cancel', bookConversation.cancel)],
    )

    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(CommandHandler("pub", pubCmd))
    
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