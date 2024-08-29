from telegram import Update
from telegram.ext import ContextTypes
import requests
from datetime import datetime, date
import structlog

logger = structlog.get_logger()


async def festivos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info(
        "Festivos command received",
        user_id=update.effective_user.id if update.effective_user else None,
        chat_id=update.effective_chat.id if update.effective_chat else None,
    )

    fiesta = None

    if update.message is not None:
        thread_id = update.message.message_thread_id
    else:
        thread_id = None

    try:
        if context.args:
            ciudad = context.args[0]
            logger.debug("Fetching holidays for city", city=ciudad)
            response = requests.get(
                url=f'http://festivos.z3r3v3r.com/{date.today().strftime("%Y")}/es/gl/{ciudad}'
            )
        else:
            logger.debug("Fetching holidays for Galicia region")
            response = requests.get(
                url=f'http://festivos.z3r3v3r.com/{date.today().strftime("%Y")}/es/gl/'
            )
        API_Data = response.json()
        logger.debug("API response received", data=API_Data)

        earliest_date = datetime.strptime(
            f'{date.today().strftime("%Y")}-12-31', "%Y-%m-%d"
        )

        for key in API_Data["datos"]:
            fecha = datetime.strptime(key["fecha"], "%Y-%m-%d")
            if fecha.date() >= date.today():
                if fecha <= earliest_date:
                    earliest_date = fecha
                    fiesta = f"O próximo festivo é {key['nombre']} o día {key['fecha']}"

        if update.effective_chat is not None:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=fiesta or "Error ao buscar festivos",
                message_thread_id=thread_id,
            )
            logger.info(
                "Sent holiday information",
                chat_id=update.effective_chat.id,
                message=fiesta,
            )
    except Exception as e:
        if update.effective_chat is not None:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="O lugar solicitado non é valido",
                message_thread_id=thread_id,
            )
        logger.error(
            "An error occurred while fetching holidays",
            error=str(e),
            user_id=update.effective_user.id if update.effective_user else None,
            chat_id=update.effective_chat.id if update.effective_chat else None,
        )
