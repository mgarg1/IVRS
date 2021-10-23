from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler

TELEGRAM_HTTP_API_TOKEN = 'token'

FIRST, SECOND, HELP = range(3)

def start(bot, update):
    keyboard = [
        [InlineKeyboardButton(u"Next", callback_data=str(FIRST))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        u"Start handler, Press next",
        reply_markup=reply_markup
    )
    return FIRST

def first(bot, update):
    query = update.callback_query
    #reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(chat_id=query.message.chat_id,
                        text='hi')

def help(bot,update):
    keyboard = [
        [InlineKeyboardButton(u"HELP", callback_data=str(HELP))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        u"Help handler, Press button",
        reply_markup=reply_markup
    )

    return HELP

def myhelp(bot,update):
    query = update.callback_query
    bot.send_message(chat_id=query.message.chat_id,
                        text='help')

updater = Updater(TELEGRAM_HTTP_API_TOKEN)

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        FIRST: [CallbackQueryHandler(first)]
    },
    fallbacks=[CommandHandler('start', start)]
)
conv_handler1=ConversationHandler(
    entry_points=[CommandHandler('help',help)],
    states={
        HELP: [CallbackQueryHandler(myhelp)]
    },
    fallbacks=[CommandHandler('help',help)]
)

updater.dispatcher.add_handler(conv_handler)
updater.dispatcher.add_handler(conv_handler1)

updater.start_polling()

updater.idle()