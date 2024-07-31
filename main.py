from telegram.ext import CommandHandler, ApplicationBuilder, MessageHandler, filters

from start import start
from newmembers import new_members
from cerveza import cerveza, cervezahora, cervezalugar, cervezamapa, cervezaasistencia,cervezalink
from help import help
from pina import pinacolada
from fiestas import festivos
from karma import kup, kdown, kshow, klist
from dinner import startDinner, dinnerOrder, roundOrder, changePrice, endDinner, beerTaker, changeMenu, removeItemOrder
import tracemalloc
import os
tracemalloc.start()


def get_bot_token():
    return os.environ['BOT_TOKEN']
    # return '6836403587:AAFaoLBovQo-Sd69RcgUk_uFTkZctRcyqZY'


def main():
    # Create an updater object with your bot's token
    application = ApplicationBuilder().token(get_bot_token()).build()

    # Add a handler for the new member entering the chat
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_members))

    commands = {
        'beer': beerTaker,
        'cerveza': cerveza,
        'cervezahora': cervezahora,
        'cervezaasistencia': cervezaasistencia,
        'cervezalugar': cervezalugar,
        'cervezamapa': cervezamapa,
        'cervezalink': cervezalink,
        'enddinner': endDinner,
        'festivos': festivos,
        'help': help,
        'kup': kup,
        'kdown': kdown,
        'klist': klist,
        'kshow': kshow,
        "menuchange": changeMenu,
        'order': dinnerOrder,
        "orderchange": removeItemOrder,
        'pineapple': pinacolada,
        'pricechange': changePrice,
        'roundOrder': roundOrder,
        'start': start,
        'startdinner': startDinner,
    }

    for comm_string, funct in commands.items():
        application.add_handler(CommandHandler(comm_string, funct))

    # Start the Bot
    application.run_polling()


if __name__ == '__main__':
    main()
