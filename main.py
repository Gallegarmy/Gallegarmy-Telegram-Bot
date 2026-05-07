from telegram.ext import (
    CommandHandler,
    ApplicationBuilder,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    ContextTypes,
)
from telegram.error import Conflict, NetworkError

from telegram_bot.karma.modify_karma import kup, kdown, klist, kshow
from telegram_bot.db.db_handler import DbHandler
from telegram_bot.start import start
from telegram_bot.callout import vigo, coruna
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
from telegram_bot.steam import steam_game
import tracemalloc
from dotenv import load_dotenv
import os

tracemalloc.start()

REQUEST_TIMEOUT = 60
GET_UPDATES_TIMEOUT = 30


def get_bot_token():
    token = os.environ.get("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN is required")
    logger.info("Bot token retrieved successfully")
    return token


async def handle_application_error(
    update: object, context: ContextTypes.DEFAULT_TYPE
) -> None:
    error = context.error
    if isinstance(error, NetworkError) and update is None:
        logger.warning("Telegram polling network error", error=str(error))
        return
    if isinstance(error, Conflict) and update is None:
        logger.error(
            "Telegram polling conflict; another bot instance is using this token",
            error=str(error),
        )
        return

    logger.error(
        "Unhandled Telegram bot error",
        error=str(error),
        update_type=type(update).__name__ if update is not None else None,
    )


def main():
    logger.info("Starting the bot application")

    # Load environment variables
    load_dotenv()

    # Initialize the connection pool
    DbHandler.initialize_pool(pool_size=10)

    logger.info("Database connection pool initialized")

    # Create an updater object with your bot's token
    application = (
        ApplicationBuilder()
        .token(get_bot_token())
        .read_timeout(REQUEST_TIMEOUT)
        .write_timeout(REQUEST_TIMEOUT)
        .connect_timeout(REQUEST_TIMEOUT)
        .pool_timeout(REQUEST_TIMEOUT)
        .get_updates_read_timeout(GET_UPDATES_TIMEOUT)
        .get_updates_write_timeout(GET_UPDATES_TIMEOUT)
        .get_updates_connect_timeout(GET_UPDATES_TIMEOUT)
        .get_updates_pool_timeout(GET_UPDATES_TIMEOUT)
        .build()
    )

    logger.info("Application built")

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
        "vigo": vigo,
        "coruna": coruna,
        "steam": steam_game,
    }

    for comm_string, funct in commands.items():
        application.add_handler(CommandHandler(comm_string, funct))
        logger.info("Command registered", command=comm_string, handler=funct.__name__)

    application.add_error_handler(handle_application_error)
    logger.info("Application error handler registered")

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
