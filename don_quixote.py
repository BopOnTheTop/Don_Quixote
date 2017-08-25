from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
import time
import logging
from telegram.ext import Updater
from telegram.ext import CommandHandler
from pathlib import Path




configs = [
    "./settings.conf",
    "/etc/don_quixote/settings.conf"

]
settings = {}
localization = {}
def read_settings():

    for config in configs:
        config_path = Path(config)
        if config_path.is_file():
            exec(open(config).read(), settings)
    #checking if  needed tokens exist
    if not "telegram_token" in settings:
        exit(1)
    elif not "sancho_disguise" in settings:
        exit(1)
    else:
        #print(settings['sancho_disguise'], settings['telegram_token'])
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
        localization_path = Path(settings['localization']+".py")
        if localization_path.is_file():
            exec(open(settings['localization']+".py").read(), localization)


def help(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=localization['help'])


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=localization['sancho_hello'])


def windmills(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=msg)
    pass


def strange_windmills(bot, update):
    pass


def what(bot, update):
    pass


def trabajo(bot, update):
    pass


def pendejo(bot, update, args):
    time_mins = args[0]
    message_arg = args[1:]
    message = 'Ти сказав мені: "{message}".\nЩо би це значило?'.format(message=message_arg)
    time.sleep(int(time_mins)*60)
    bot.send_message(chat_id=update.message.chat_id, text=message)
    pass


def film(bot, update):
    pass


def main():

    updater = Updater(token=settings['telegram_token'])
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    help_handler = CommandHandler('help', help)
    dispatcher.add_handler(help_handler)

    pendejo_handler = CommandHandler('pendejo', pendejo, pass_args=True)
    dispatcher.add_handler(pendejo_handler)
    updater.start_polling()

read_settings()
main()


