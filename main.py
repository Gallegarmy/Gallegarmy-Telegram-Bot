from telegram.ext import (
    CommandHandler,
    ApplicationBuilder,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)

from telegram_bot.start import start
from telegram_bot.status import ping
from telegram_bot.newmembers import new_members
from telegram_bot.cerveza import (
    cerveza,
    cervezahora,
    cervezalugar,
    cervezamapa,
    cervezaasistencia,
    cervezalink,
)
from telegram_bot.help import help
from telegram_bot.pina import pinacolada
from telegram_bot.fiestas import festivos
from telegram_bot.karma import kup, kdown, kshow, klist
from telegram_bot.dinner import (
    startDinner,
    roundOrder,
    changePrice,
    endDinner,
    beerTaker,
    changeMenu,
    dinnerOrder,
    removeItemOrder,
    show_dinner_keyboard,
    dinnerkeyb_handler,
    dinnerTaker,
)
import tracemalloc
from dotenv import load_dotenv
import os

tracemalloc.start()


def get_bot_token():
    return os.environ["BOT_TOKEN"]


def main():
    # Create an updater object with your bot's token
    application = ApplicationBuilder().token(get_bot_token()).build()

    commands = {
        "beer": beerTaker,
        "dinner": dinnerTaker,
        "cerveza": cerveza,
        "cervezahora": cervezahora,
        "cervezaasistencia": cervezaasistencia,
        "cervezalugar": cervezalugar,
        "cervezamapa": cervezamapa,
        "cervezalink": cervezalink,
        "enddinner": endDinner,
        "festivos": festivos,
        "help": help,
        "kup": kup,
        "kdown": kdown,
        "klist": klist,
        "kshow": kshow,
        "menuchange": changeMenu,
        "order": dinnerOrder,
        "orderchange": removeItemOrder,
        "pineapple": pinacolada,
        "pricechange": changePrice,
        "roundOrder": roundOrder,
        "start": start,
        "startdinner": startDinner,
        "ping": ping,
    }

    for comm_string, funct in commands.items():
        application.add_handler(CommandHandler(comm_string, funct))

    # Exemplo minimo de teclado
    # TODO Mover ao dict de arriba
    application.add_handler(CommandHandler("teclado", show_dinner_keyboard))

    application.add_handler(
        CallbackQueryHandler(
            dinnerkeyb_handler,
        )
    )

    # Add a handler for the new member entering the chat
    application.add_handler(
        MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_members)
    )

    # Start the Bot
    application.run_polling()


if __name__ == "__main__":
    load_dotenv()
    main()
