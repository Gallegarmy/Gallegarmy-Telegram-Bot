from telegram import Update
from telegram.ext import ContextTypes
import requests
import structlog
from urllib.parse import quote_plus

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
            game = quote_plus(" ".join(context.args).replace("_", " "))
            logger.debug("Fetching results for game", steam_game=game)
            response = requests.get(
                url=f"https://store.steampowered.com/api/storesearch/?term={game}&l=english&cc=es",
                timeout=10,
            )
            response.raise_for_status()
        else:
            logger.debug("No game was provided")
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Necesito un xogo para poder traer información sobre el.",
                message_thread_id=thread_id,
            )
            return

        data = response.json()
        items = data.get("items", [])
        if items:
            first = items[0]

            name = first.get("name")

            price_info = first.get("price", {})
            price = price_info.get("final")
            currency = price_info.get("currency", "EUR")
            if price is None:
                price = "Non dispoñible"
            elif price == 0:
                price = "Gratis"
            else:
                price = str(price).zfill(3)
                price = f"{price[:-2]},{price[-2:]} {currency}"

            platforms = first.get("platforms", {})
            windows = platforms.get("windows")
            windows = ":)" if windows else ":("
            mac = platforms.get("mac")
            mac = ":)" if mac else ":("
            linux = platforms.get("linux")
            linux = ":)" if linux else ":("

            message = (
                f"Titulo: {name}\n\n"
                f"Prezo: {price}\n"
                f"Plataformas:\nLinux: {linux}\nWindows: {windows}\nMac: {mac}"
            )
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=message,
                message_thread_id=thread_id,
            )

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
