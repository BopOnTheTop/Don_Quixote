from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
import time
import logging
from telegram.ext import Updater
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Filters, Job
from pathlib import Path




configs = [
    "./settings.conf",
    "/etc/don_quixote/settings.conf"

]
settings = {}
localization = {}
time_msg = ""
msg_text = ""
# Pendejo job stats
PENDEJO, PENDEJO_TIME, PENDEJO_MESSAGE = range(3)

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





def pendejo(bot, update):
    update.message.reply_text(localization['pendejo_start'])
    return PENDEJO_TIME


def pendejo_get_time(bot, update):
    global time_msg
    time_msg = update.message.text
    update.message.reply_text(localization['pendejo_time'])
    return PENDEJO_MESSAGE


def pendejo_get_message(bot, update, job_queue):
    global time_msg
    global msg_text
    msg_text = update.message.text
    update.message.reply_text(localization['pendejo_msg'].format(time=time_msg, text=msg_text))

    #TODO: Introduce comdined tiem def. Like "1h (and) 10 minutes".
    #TODO: Make the quantum comparation set more... localized.
    #TODO: Make quantum comparation less hardcoded. Currentlu it looks not that neat as
    # I would like it to be.
    time_msg = time_msg.split(" ")
    time = time_msg[0]
    quantum = time_msg[1]
    if quantum == "min" or quantum == "Min" or quantum == "хв" or quantum == "Хв" \
        or quantum == "хвилин":
        # Job callback understands this value as minutes in default.
        pass

    job_pendejo = Job(pendejo_callback, 60.0, repeat = False, context = update.message.chat_id)
    job_queue.put(job_pendejo)
    return ConversationHandler.END


def pendejo_callback(bot, job):



def cancel(bot, update):
    update.message.reply_text(localization['pendejo_cancel'])
    return ConversationHandler.END


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

    pendejo_handler = ConversationHandler(
        entry_points=[CommandHandler('pendejo', pendejo)],

        states={

            PENDEJO_TIME: [MessageHandler(Filters.text, pendejo_get_time)],
            PENDEJO_MESSAGE: [MessageHandler(Filters.text, pendejo_get_message, pass_job_queue=True)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    #pendejo_handler = CommandHandler('pendejo', pendejo, pass_args=True)
    dispatcher.add_handler(pendejo_handler)


    updater.start_polling()

read_settings()
main()


