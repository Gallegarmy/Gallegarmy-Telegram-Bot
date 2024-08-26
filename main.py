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
    cerveza_hora,
    cerveza_lugar,
    cerveza_mapa,
    cerveza_asistencia,
    cerveza_link,
)
from telegram_bot.help import help
from telegram_bot.pina import pinacolada
from telegram_bot.fiestas import festivos
from telegram_bot.karma import kup, kdown, kshow, klist, initialize_db

initialize_db()
from telegram_bot.dinner import (
    start_dinner,
    round_order,
    change_price,
    end_dinner,
    beer_taker,
    change_menu,
    dinner_order,
    remove_item_order,
    show_dinner_keyboard,
    dinner_keyboard_handler,
    dinner_taker,
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
        "beer": beer_taker,
        "dinner": dinner_taker,
        "cerveza": cerveza,
        "cervezahora": cerveza_hora,
        "cervezaasistencia": cerveza_asistencia,
        "cervezalugar": cerveza_lugar,
        "cervezamapa": cerveza_mapa,
        "cervezalink": cerveza_link,
        "enddinner": end_dinner,
        "festivos": festivos,
        "help": help,
        "kup": kup,
        "kdown": kdown,
        "klist": klist,
        "kshow": kshow,
        "menuchange": change_menu,
        "order": dinner_order,
        "orderchange": remove_item_order,
        "pineapple": pinacolada,
        "pricechange": change_price,
        "roundOrder": round_order,
        "start": start,
        "startdinner": start_dinner,
        "ping": ping,
    }

    for comm_string, funct in commands.items():
        application.add_handler(CommandHandler(comm_string, funct))

    # Exemplo minimo de teclado
    # TODO Mover ao dict de arriba
    application.add_handler(CommandHandler("teclado", show_dinner_keyboard))

    application.add_handler(
        CallbackQueryHandler(
            dinner_keyboard_handler,
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
