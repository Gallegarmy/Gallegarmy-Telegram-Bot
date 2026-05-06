from telegram import Update
from telegram.ext import ContextTypes
import requests
import structlog

logger = structlog.get_logger()


async def steam_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(
        "Steam command received",
        user_id=update.effective_user.id if update.effective_user else None,
        chat_id=update.effective_chat.id if update.effective_chat else None,
    )

    if update.message is not None:
        thread_id = update.message.message_thread_id
    else:
        thread_id = None

    try:
        if context.args:
            game = context.args[0]
            game = game.replace("_", "%20")
            logger.debug("Fetching results for game", steam_game=game)
            response = requests.get(
                url=f'https://store.steampowered.com/api/storesearch/?term={game}&l=english&cc=es'
            )
        else:
            logger.debug("No game was provided")
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Necesito un xogo para poder traer información sobre el.",
                message_thread_id=thread_id,
            )
            return
        
        data = res.json()
        if data["items"]:
            game_title = data["items"][0]

            name = first.get("name")

            price_info = first.get("price", {})
            currency = price_info.get("currency")
            price = price_info.get("final")
            price = price.zfill(3)
            price = price[:-2] + "," + price[-2:]

            platforms = first.get("platforms", {})
            windows = platforms.get("windows")
            windows = ":)" if windows else ":("
            mac = platforms.get("mac")
            mac = ":)" if mac else ":("
            linux = platforms.get("linux")
            linux = ":)" if linux else ":("
            
            message='Titulo: {name}\n\nPrezo: {price} {currency}\nPlataformas:\nLinux: {linux}\nWindows: {windows}\nMan: {mac}'

        else:
            logger.debug("No game was found")
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Non atopo ese xogo en steam.",
                message_thread_id=thread_id,
            )
            return
    except Exception as e:
        if update.effective_chat is not None:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Algo saíu mal",
                message_thread_id=thread_id,
            )
        logger.error(
            "An error occurred while fetching game",
            error=str(e),
            user_id=update.effective_user.id if update.effective_user else None,
            chat_id=update.effective_chat.id if update.effective_chat else None,
        )