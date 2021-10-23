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
import constants
from dataAccess import findNextDates, isNumRegistered

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, KeyboardButton
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

def start(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks the user about their phone_number."""
    
    reply_keyboard = [[KeyboardButton(text='Share my Number', request_contact=True)]]

    update.message.reply_text(
        'Welcome to Mayuri Surgical Hospital, Dholpur\n'
        'This is our Online Appointment Service\n'
        'Here you can book for next 5 available dates\n'
        'Send /cancel anytime to stop the process. \n\n'
        'Start with sharing your number',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True
        )
    )

    return constants.ENTER_PHONE_NUM

def enter_phone_num(update: Update, context: CallbackContext) -> int:
    '''Stores the number from the shared contact'''
    
    bookingDate = None
    if "mg_data" in context.chat_data and "phone_num" in context.chat_data["mg_data"]: 
        print(context.chat_data["mg_data"])
    else:
        print(update.message.contact)
        phoneNum = update.message.contact.phone_number[-10:]  #last 10 digits
        context.chat_data["mg_data"] = {'phone_num':phoneNum}
        bookingDate = isNumRegistered(phoneNum)
        if bookingDate:
            context.chat_data['mg_data']['selected_date'] = bookingDate
            # context.chat_data['mg_data']['saved_contact'] = update.message.contact
            
            reply_keyboard = [['MODIFY'], ['DEREGISTER']]
            # print(context.chat_data["mg_data"])
            update.message.reply_text(
                'You already have an appointment on {} \n De-register or Modify the Appointment\n Send /cancel to stop. \n\n'.format(bookingDate),
                reply_markup=ReplyKeyboardMarkup(
                    reply_keyboard, one_time_keyboard=True, input_field_placeholder='Choose Modify/De-register?'
                ),
            )
            return constants.ALREADY_REGISTERED

    # print('REACHED HERE')
    dates = findNextDates()
    reply_keyboard = [ [individualArray] for individualArray in dates]
    update.message.reply_text(
        'aapka number .... use kiya jayega \n ab date select kijiye \n Send /cancel to stop. \n\n',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Choose a date?'
        ),
    )

    return constants.SEL_DATE

def alreadyRegistered(update: Update, context: CallbackContext) -> int:
    isModify = update.message.text
    selDate = context.chat_data['mg_data']['selected_date']
    print('isConfirmed--> ' + isModify)
    if isModify == 'MODIFY':
        update.message.reply_text(
            'You selected MODIFY,Choose new Dates\n\n',
            reply_markup=ReplyKeyboardRemove()
        )
        return enter_phone_num(update, context)
    
    if isModify == 'DEREGISTER':
         update.message.reply_text(
            'You selected DEREGISTER,Cancelling your appointment for {}\n\n'.format(selDate),
            reply_markup=ReplyKeyboardRemove()
        )
    
    return ConversationHandler.END

def selectDate(update: Update, context: CallbackContext) -> int:
    """Stores the selected date and asks for confirmation."""
    selectedDate = update.message.text
    context.chat_data['mg_data']['selected_date'] = selectedDate

    reply_keyboard = [['YES', 'NO']]
    # print(context.chat_data["mg_data"])
    update.message.reply_text(
        'You selected {} \n Click on Yes to Confirm and No to choose again\n Send /cancel to stop. \n\n'.format(selectedDate),
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Confirm Yes/NO?'
        ),
    )

    return constants.CONFIRM_DATE

def confirmDate(update: Update, context: CallbackContext) -> int:
    '''Books the appointment or re-select the date'''
    isConfirmed = update.message.text
    print('isConfirmed-->' + isConfirmed)
    if isConfirmed == 'YES':
        update.message.reply_text(
            'You selected Yes,Booking your appointment',
            reply_markup=ReplyKeyboardRemove()
        )
        return book_appointment(update, context)
        # return constants.CONFIRMATION
    else:
        update.message.reply_text(
            'Please re-select the date',
            reply_markup=ReplyKeyboardRemove()
        )
        return enter_phone_num(update, context)
        # return constants.ENTER_PHONE_NUM
    
def book_appointment(update: Update, context: CallbackContext):
    print('booking appointment')
    update.message.reply_text(
        'Apt confirmed for {} for date {}\n\n'.format(context.chat_data['mg_data']['phone_num'], context.chat_data['mg_data']['selected_date']),
        reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END