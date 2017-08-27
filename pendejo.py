from __future__ import absolute_import
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
import logging
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, Filters, Job
from settings import settings,localization

time_msg = ""
msg_text = ""
# Pendejo job stats
PENDEJO, PENDEJO_TIME, PENDEJO_MESSAGE = range(3)



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

    #TODO: Introduce comdined tiem def. Like "1h (and) 10 minutes".
    #TODO: Make the quantum comparation set more... localized.
    time_msg = time_msg.split(" ")
    time = float(time_msg[0])
    quantum = time_msg[1]
    print(quantum)
    print(localization['quantum_minute'])
    if quantum in localization['quantum_minute']:
        # Job callback understands this value as seconds by default.
        time *= 60
        pass

    elif quantum in localization['quantum_hour']:
        # Multiplying hours by 60 soat the end we will have minutes. Suddenly.
        time *= 3600

    logging.info("Spawned a time:{time} delayed message:{message}".format(time=time,message=msg_text))
    update.message.reply_text(localization['pendejo_msg'].format(time=time))

    job_queue.run_once(pendejo_callback, when=time, context=update.message.chat_id)
    return ConversationHandler.END


def pendejo_callback(bot, job):
    response = localization['pendejo_callback'].format(message=msg_text)
    bot.send_message(chat_id=job.context, text=response)


def pendejo_cancel(bot, update):
    update.message.reply_text(localization['pendejo_cancel'])
    return ConversationHandler.END


pendejo_handler = ConversationHandler(
        entry_points=[CommandHandler('pendejo', pendejo)],
        states={
            PENDEJO_TIME: [MessageHandler(Filters.text, pendejo_get_time)],
            PENDEJO_MESSAGE: [MessageHandler(Filters.text, pendejo_get_message, pass_job_queue=True)]
        },
        fallbacks=[CommandHandler('cancel', pendejo_cancel)]
    )