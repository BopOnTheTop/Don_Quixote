from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
import time
import logging
from telegram.ext import Updater
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Filters, Job
from pathlib import Path
from settings import settings,localization
from pendejo import pendejo_handler
import os

def help(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=localization['help'])


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=localization['sancho_hello'])


def windmills(bot, update):
    msg = os.popen("fortune ").read()
    bot.send_message(chat_id=update.message.chat_id, text=msg)
    pass


def strange_windmills(bot, update):
    pass


def what(bot, update):
    pass


def trabajo(bot, update):
    pass



def film(bot, update):
    """
    Looks like film management will be in a separate file. As `pendejo` code shown.
    :param bot:
    :param update:
    :return:
    """
    pass


def error(bot, update, error):
    logging.warning('Update "%s" caused error "%s"' % (update, error))
    update.message.reply_text(localization['something_went_wrong'])


def main():

    print(settings['telegram_token'])
    updater = Updater(token=settings['telegram_token'])
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    help_handler = CommandHandler('help', help)
    dispatcher.add_handler(help_handler)

    windmills_handler = CommandHandler('windmills', windmills)
    dispatcher.add_handler(windmills_handler)
    dispatcher.add_handler(pendejo_handler)
    dispatcher.add_error_handler(error)

    updater.start_polling()

main()


