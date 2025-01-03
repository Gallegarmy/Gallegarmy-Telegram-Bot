from telegram.ext import (
    CommandHandler,
    ApplicationBuilder,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)

from telegram_bot.karma.modify_karma import kup, kdown, klist, kshow
from telegram_bot.db.db_handler import DbHandler
from telegram_bot.start import start
from telegram_bot.status import ping
from telegram_bot.newmembers import new_members
from telegram_bot.events.events_handler import events
from telegram_bot.help import help
from telegram_bot.pina import pinacolada
from telegram_bot.fiestas import festivos
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
from telegram_bot.utils.logger import logger
import tracemalloc
from dotenv import load_dotenv
import os
import structlog
import logging

tracemalloc.start()




def get_bot_token():
    token = os.environ["BOT_TOKEN"]
    logger.info("Bot token retrieved successfully")
    return token


def main():
    logger.info("Starting the bot application")

    # Load environment variables
    load_dotenv()    

    #Initialize the connection pool
    DbHandler.initialize_pool(pool_size=10)

    logger.info("Database connection pool initialized")

    # Create an updater object with your bot's token
    application = ApplicationBuilder().token(get_bot_token()).read_timeout(60).write_timeout(60).build()

    logger.info("Application built", token=get_bot_token())

    commands = {
        "beer": beer_taker,
        "dinner": dinner_taker,
        "events": events,
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
        logger.info("Command registered", command=comm_string, handler=funct.__name__)

    application.add_handler(CommandHandler("teclado", show_dinner_keyboard))
    logger.info(
        "Command registered", command="teclado", handler=show_dinner_keyboard.__name__
    )

    application.add_handler(
        CallbackQueryHandler(
            dinner_keyboard_handler,
        )
    )
    logger.info("CallbackQueryHandler registered for dinner_keyboard_handler")

    application.add_handler(
        MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_members)
    )
    logger.info("MessageHandler registered for new chat members")

    logger.info("Starting bot polling")
    application.run_polling()
    logger.info("Bot polling started successfully")


if __name__ == "__main__":
    main()
