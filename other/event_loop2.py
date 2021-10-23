  
#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import Update, ForceReply, InlineKeyboardMarkup
from telegram import InlineKeyboardButton as Button
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
import  sensitive


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )

def reserve():
    buttons = [Button(text="1",callback_data='1'),Button(text="2",callback_data='2'),Button(text="3",callback_data='3')]
    return InlineKeyboardMarkup(buttons)


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    # keyboard = [[InlineKeyboardButton("Hackerearth", callback_data='HElist8'),
    #                      InlineKeyboardButton("Hackerrank", callback_data='HRlist8')],
    #                     [InlineKeyboardButton("Codechef", callback_data='CClist8'),
    #                      InlineKeyboardButton("Spoj", callback_data='SPlist8')],
    #                     [InlineKeyboardButton("Codeforces", callback_data='CFlist8'),
    #                      InlineKeyboardButton("ALL", callback_data='ALLlist8')]]

    buttons = [[Button("1111",callback_data='selected 1')],[Button("22222",callback_data='selected  2')],[Button("333333",callback_data='selected 3')]]
    print(InlineKeyboardMarkup(buttons))
    update.message.reply_text('Response',reply_markup=InlineKeyboardMarkup(buttons))


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def print22(update: Update, context: CallbackContext):
    print('<-------- Print a ------------> \n\n')
    print(update)
    print('\n\n<-------- Print b ------------> \n\n')
    print(context)



def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    token22 = sensitive.TELEGRAM_BOT_ID + ':' + sensitive.TELEGRAM_AUTH_TOKEN
    updater = Updater(token=token22)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    # dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CallbackQueryHandler(print22, pattern='^selected'))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()


# from telegram import Update
# from telegram.ext import Updater, CommandHandler, CallbackContext
# import sensitive

# def hello(update: Update, context: CallbackContext) -> None:
#     update.message.reply_text(f'Hello {update.effective_user.first_name}')


# updater = Updater(token=token22)

# updater.dispatcher.add_handler(CommandHandler('hello', hello))

# updater.start_polling()
# updater.idle()