import os
import mysql.connector
from telegram import Update
from telegram.ext import ContextTypes
from collections import defaultdict
import datetime
import structlog
import functools

from telegram_bot.utils.tgram_utils import get_user

logger = structlog.get_logger()

karmaLimit = defaultdict(int)
last_cleared_date = None
CHAT_ID = -1001920687768
TEST_MODE = os.getenv("TEST_MODE") == "true"

def async_only_sysarmy_chat(func):
    """
    Decorator to ensure requests are only handled in Sysarmy to avoid centryk exploits.
    """

    @functools.wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if TEST_MODE:
            return await func(update, context)

        if (
            update.effective_message
            and update.effective_message.chat_id == CHAT_ID
        ):
            logger.info(
                "Handling request in Sysarmy chat",
                user_id=update.effective_user.id if update.effective_user else None,
                chat_id=update.effective_chat.id if update.effective_chat else None,
            )
            return await func(update, context)
        else:
            logger.warning(
                "Request not in Sysarmy Chat",
                user_id=update.effective_user.id if update.effective_user else None,
                chat_id=update.effective_chat.id if update.effective_chat else None,
            )

    return wrapper


async def karma(update: Update, context: ContextTypes.DEFAULT_TYPE, operation: str):
    global karmaLimit, last_cleared_date
    now = datetime.datetime.now()
    if last_cleared_date is None or now.date() > last_cleared_date:
        karmaLimit.clear()
        last_cleared_date = now.date()
        logger.debug("Karma limits cleared", date=last_cleared_date)

    executing_username = update.message.from_user.username  
    if update.message and update.message.from_user and update.effective_chat:
        thread_id = update.message.message_thread_id

        target_username = ''
        if update.message.reply_to_message is not None:
            detected_user = update.effective_message.reply_to_message.from_user
            if detected_user:
                target_username = detected_user.username or detected_user.first_name
        elif context.args:
            target_username = str(context.args[0])


        if target_username:
            is_user = target_username[0] == '@'
            target_username = target_username.lower().removeprefix('@')
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Necesito un usuario para asignarlle/quitarlle karma",
                message_thread_id=thread_id,
            )
            logger.warning(
                "Karma command received without arguments",
                user_id=update.effective_user.id if update.effective_user else None,
            )
            return None

        if target_username == executing_username.lower():
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Non sexas tan egocéntrico tío",
                message_thread_id=thread_id,
            )
            logger.warning(
                "User tried to give/remove karma to themselves",
                user=executing_username,
            )
            return None

        if executing_username not in karmaLimit:
            karmaLimit[executing_username] = 5

        if karmaLimit[executing_username] == 0:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Xa non podes asignar/quitar máis karma hoxe",
                message_thread_id=thread_id,
            )
            logger.info(
                "Karma limit reached", user=executing_username
            )
            return None

        database = mysql.connector.connect(
            host=os.environ.get("MYSQL_HOST"),
            user=os.environ.get("MYSQL_USER"),
            password=os.environ.get("MYSQL_PASSWORD"),
            database=os.environ.get("MYSQL_DATABASE"),
        )
        cursor = database.cursor()
        SQLUsers = "SELECT * FROM karma WHERE word = %s"
        cursor.execute(SQLUsers, (target_username,))
        usuarios = cursor.fetchall()

        if len(usuarios) == 0:
            if operation == "add":
                SQLCreateuser = "INSERT INTO karma (word, karma, is_user) VALUES (%s, 1, %s)"
                cursor.execute(SQLCreateuser, (target_username, is_user))
                logger.info("New user created in karma database", user=target_username)
            elif operation == "remove":
                SQLCreateuser = "INSERT INTO karma (word, karma, is_user) VALUES (%s, -1, %s)"
                cursor.execute(SQLCreateuser, (target_username, is_user))
                logger.info("New user created in karma database", user=target_username)
        else:
            if operation == "add":
                SQLAddKarma = "UPDATE karma SET karma = karma + 1 WHERE word = %s"
                cursor.execute(SQLAddKarma, (target_username,))
                logger.info("Karma increased for user", user=target_username)
            elif operation == "remove":
                SQLAddKarma = "UPDATE karma SET karma = karma - 1 WHERE word = %s"
                cursor.execute(SQLAddKarma, (target_username,))
                logger.info("Karma decreased for user", user=target_username)

        database.commit()
        database.close()
        karmaLimit[executing_username] -= 1
        return [target_username, thread_id]
    

@async_only_sysarmy_chat
async def kup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(
        "Karma up command received",
        user_id=update.effective_user.id if update.effective_user else None,
        chat_id=update.effective_chat.id if update.effective_chat else None,
    )

    response_status = await karma(update, context, "add")
    
    if response_status is not None:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"+1 Karma para {response_status[0]}",
            message_thread_id=response_status[1],
        )


@async_only_sysarmy_chat
async def kdown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(
        "Karma down command received",
        user_id=update.effective_user.id if update.effective_user else None,
        chat_id=update.effective_chat.id if update.effective_chat else None,
    )

    response_status = await karma(update, context, "remove")
    
    if response_status is not None:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"-1 Karma para {response_status[0]}",
            message_thread_id=response_status[1],
        )

@async_only_sysarmy_chat
async def kshow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(
        "Karma show command received",
        user_id=update.effective_user.id if update.effective_user else None,
        chat_id=update.effective_chat.id if update.effective_chat else None,
    )

    if update.message and update.effective_chat:
        thread_id = update.message.message_thread_id
        if context.args:
            usuario = str(context.args[0])
            logger.debug("Show karma for user/word requested", target=usuario)

            database = mysql.connector.connect(
                host=os.environ.get("MYSQL_HOST"),
                user=os.environ.get("MYSQL_USER"),
                password=os.environ.get("MYSQL_PASSWORD"),
                database=os.environ.get("MYSQL_DATABASE"),
            )
            cursor = database.cursor()

            if usuario[0] == "@":
                usuario = usuario[1:]
                SQLUsers = "SELECT karma FROM karma WHERE word = %s"
                cursor.execute(SQLUsers, (usuario.lower(),))
                karma_result = cursor.fetchone()

                if karma_result is None:
                    SQLCreateuser = (
                        "INSERT INTO karma (word, karma, is_user) VALUES (%s, 0, true)"
                    )
                    cursor.execute(SQLCreateuser, (usuario.lower(),))
                    logger.info("User created with zero karma", user=usuario.lower())
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"El Karma de {usuario.lower()} es 0",
                        message_thread_id=thread_id,
                    )
                else:
                    (karma,) = karma_result
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"El Karma de {usuario.lower()} es {karma}",
                        message_thread_id=thread_id,
                    )
                    logger.info("Displayed karma for user", user=usuario.lower())
            else:
                SQLUsers = "SELECT karma FROM karma WHERE word = %s"
                cursor.execute(SQLUsers, (usuario.lower(),))
                karma_result = cursor.fetchone()

                if karma_result is None:
                    SQLCreateuser = (
                        "INSERT INTO karma (word, karma, is_user) VALUES (%s, 0, false)"
                    )
                    cursor.execute(SQLCreateuser, (usuario.lower(),))
                    logger.info("Word created with zero karma", word=usuario.lower())
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"El Karma de {usuario.lower()} es 0",
                        message_thread_id=thread_id,
                    )
                else:
                    (karma,) = karma_result
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"El Karma de {usuario.lower()} es {karma}",
                        message_thread_id=thread_id,
                    )
                    logger.info("Displayed karma for word", word=usuario.lower())

            database.commit()
            database.close()
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Necesito un usuario para mostrar o seu karma",
                message_thread_id=thread_id,
            )
            logger.warning(
                "Karma show command received without arguments",
                user_id=update.effective_user.id if update.effective_user else None,
            )

@async_only_sysarmy_chat
async def klist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(
        "Karma list command received",
        user_id=update.effective_user.id if update.effective_user else None,
        chat_id=update.effective_chat.id if update.effective_chat else None,
    )

    if update.message and update.effective_chat:
        thread_id = update.message.message_thread_id
        karma_list = "Usuarios con más karma:\n\n"

        database = mysql.connector.connect(
            host=os.environ.get("MYSQL_HOST"),
            user=os.environ.get("MYSQL_USER"),
            password=os.environ.get("MYSQL_PASSWORD"),
            database=os.environ.get("MYSQL_DATABASE"),
        )
        cursor = database.cursor()

        SQLPrimeros = "SELECT word, karma FROM karma WHERE is_user = true ORDER BY karma DESC LIMIT 3"
        cursor.execute(SQLPrimeros)
        users = cursor.fetchall()

        for user in users:
            word, karma = user  # Correctly unpack the tuple
            karma_list += f"{word}: {karma}\n"
        logger.info("Top users with karma retrieved", users=users)

        karma_list += "\nPalabras con más karma:\n\n"
        SQLPrimerosPalabras = "SELECT word, karma FROM karma WHERE is_user = false ORDER BY karma DESC LIMIT 3"
        cursor.execute(SQLPrimerosPalabras)
        words = cursor.fetchall()

        for word in words:
            word_text, karma = word  # Correctly unpack the tuple
            karma_list += f"{word_text}: {karma}\n"
        logger.info("Top words with karma retrieved", words=words)

        karma_list += "\nUsuarios con menos karma:\n\n"
        SQLUltimos = "SELECT word, karma FROM karma WHERE is_user = true ORDER BY karma ASC LIMIT 3"
        cursor.execute(SQLUltimos)
        users = cursor.fetchall()

        for user in users:
            word, karma = user  # Correctly unpack the tuple
            karma_list += f"{word}: {karma}\n"
        logger.info("Bottom users with karma retrieved", users=users)

        karma_list += "\nPalabras con menos karma:\n\n"
        SQLUltimasPalabras = "SELECT word, karma FROM karma WHERE is_user = false ORDER BY karma ASC LIMIT 3"
        cursor.execute(SQLUltimasPalabras)
        words = cursor.fetchall()

        for word in words:
            word_text, karma = word  # Correctly unpack the tuple
            karma_list += f"{word_text}: {karma}\n"
        logger.info("Bottom words with karma retrieved", words=words)

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=karma_list,
            message_thread_id=thread_id,
        )
        database.close()
