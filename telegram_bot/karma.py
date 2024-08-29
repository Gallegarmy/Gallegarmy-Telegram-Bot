import os

import mysql.connector
from telegram import Update
from telegram.ext import ContextTypes
from collections import defaultdict
import datetime
import structlog

logger = structlog.get_logger()

karmaLimit = defaultdict(int)
last_cleared_date = None


async def kup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(
        "Karma up command received",
        user_id=update.effective_user.id if update.effective_user else None,
        chat_id=update.effective_chat.id if update.effective_chat else None,
    )

    global karmaLimit, last_cleared_date
    now = datetime.datetime.now()
    if last_cleared_date is None or now.date() > last_cleared_date:
        karmaLimit.clear()
        last_cleared_date = now.date()
        logger.debug("Karma limits cleared", date=last_cleared_date)

    if update.message and update.message.from_user and update.effective_chat:
        thread_id = update.message.message_thread_id
        if context.args:
            usuario = str(context.args[0])
            if usuario[0] == "@":
                usuario = usuario[1:]
                logger.debug("Karma for user requested", target_user=usuario)

                if usuario.lower() != str(update.message.from_user.username).lower():
                    if update.message.from_user.username not in karmaLimit:
                        karmaLimit[update.message.from_user.username] = 5

                    if karmaLimit[update.message.from_user.username] == 0:
                        await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text="Xa non podes asignar máis karma hoxe",
                            message_thread_id=thread_id,
                        )
                        logger.info(
                            "Karma limit reached",
                            user=update.message.from_user.username,
                        )
                        return

                    database = mysql.connector.connect(
                        host=os.environ.get('MYSQL_HOST'),
                        user=os.environ.get('MYSQL_USER'),
                        password=os.environ.get('MYSQL_PASSWORD'),
                        database=os.environ.get('MYSQL_DATABASE'),
                    )
                    cursor = database.cursor()
                    SQLUsers = "SELECT * FROM karma WHERE word = %s"
                    cursor.execute(SQLUsers, (usuario.lower(),))
                    usuarios = cursor.fetchall()

                    if len(usuarios) == 0:
                        SQLCreateuser = "INSERT INTO karma (word, karma, is_user) VALUES (%s,1, true)"
                        cursor.execute(SQLCreateuser, (usuario.lower(),))
                        logger.info(
                            "New user created in karma database", user=usuario.lower()
                        )
                    else:
                        SQLAddKarma = (
                            "UPDATE karma SET karma = karma + 1 WHERE word = %s"
                        )
                        cursor.execute(SQLAddKarma, (usuario.lower(),))
                        logger.info("Karma increased for user", user=usuario.lower())

                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"+1 Karma para {usuario.lower()}",
                        message_thread_id=thread_id,
                    )
                    database.commit()
                    database.close()
                    karmaLimit[update.message.from_user.username] -= 1
                else:
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Non sexas tan egocéntrico tío",
                        message_thread_id=thread_id,
                    )
                    logger.warning(
                        "User tried to give karma to themselves",
                        user=update.message.from_user.username,
                    )
            else:
                if update.message.from_user.username not in karmaLimit:
                    karmaLimit[update.message.from_user.username] = 5

                if karmaLimit[update.message.from_user.username] == 0:
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Xa non podes asignar máis karma hoxe",
                        message_thread_id=thread_id,
                    )
                    logger.info(
                        "Karma limit reached", user=update.message.from_user.username
                    )
                    return

                database = mysql.connector.connect(
                    host=os.environ.get('MYSQL_HOST'),
                    user=os.environ.get('MYSQL_USER'),
                    password=os.environ.get('MYSQL_PASSWORD'),
                    database=os.environ.get('MYSQL_DATABASE'),
                )
                cursor = database.cursor()
                SQLUsers = "SELECT * FROM karma WHERE word = %s"
                cursor.execute(SQLUsers, (usuario.lower(),))
                usuarios = cursor.fetchall()

                if len(usuarios) == 0:
                    SQLCreateuser = (
                        "INSERT INTO karma (word, karma, is_user) VALUES (%s,1, false)"
                    )
                    cursor.execute(SQLCreateuser, (usuario.lower(),))
                    logger.info(
                        "New word created in karma database", word=usuario.lower()
                    )
                else:
                    SQLAddKarma = "UPDATE karma SET karma = karma + 1 WHERE word = %s"
                    cursor.execute(SQLAddKarma, (usuario.lower(),))
                    logger.info("Karma increased for word", word=usuario.lower())

                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"+1 Karma a {usuario.lower()}",
                    message_thread_id=thread_id,
                )
                database.commit()
                database.close()
                karmaLimit[update.message.from_user.username] -= 1
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Necesito un usuario para asignarlle karma",
                message_thread_id=thread_id,
            )
            logger.warning(
                "Karma up command received without arguments",
                user_id=update.effective_user.id if update.effective_user else None,
            )


async def kdown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(
        "Karma down command received",
        user_id=update.effective_user.id if update.effective_user else None,
        chat_id=update.effective_chat.id if update.effective_chat else None,
    )

    global karmaLimit, last_cleared_date
    now = datetime.datetime.now()
    if last_cleared_date is None or now.date() > last_cleared_date:
        karmaLimit.clear()
        last_cleared_date = now.date()
        logger.debug("Karma limits cleared", date=last_cleared_date)

    if update.message and update.message.from_user and update.effective_chat:
        thread_id = update.message.message_thread_id
        if context.args:
            usuario = str(context.args[0])
            if usuario[0] == "@":
                usuario = usuario[1:]
                logger.debug("Karma down for user requested", target_user=usuario)

                if usuario.lower() != str(update.message.from_user.username).lower():
                    if update.message.from_user.username not in karmaLimit:
                        karmaLimit[update.message.from_user.username] = 5

                    if karmaLimit[update.message.from_user.username] == 0:
                        await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text="Xa non podes asignar máis karma hoxe",
                            message_thread_id=thread_id,
                        )
                        logger.info(
                            "Karma limit reached",
                            user=update.message.from_user.username,
                        )
                        return

                    database = mysql.connector.connect(
                        host=os.environ.get('MYSQL_HOST'),
                        user=os.environ.get('MYSQL_USER'),
                        password=os.environ.get('MYSQL_PASSWORD'),
                        database=os.environ.get('MYSQL_DATABASE'),
                    )
                    cursor = database.cursor()
                    SQLUsers = "SELECT * FROM karma WHERE word = %s"
                    cursor.execute(SQLUsers, (usuario.lower(),))
                    usuarios = cursor.fetchall()

                    if len(usuarios) == 0:
                        SQLCreateuser = "INSERT INTO karma (word, karma, is_user) VALUES (%s,-1, true)"
                        cursor.execute(SQLCreateuser, (usuario.lower(),))
                        logger.info(
                            "New user created in karma database with negative karma",
                            user=usuario.lower(),
                        )
                    else:
                        SQLRemoveKarma = (
                            "UPDATE karma SET karma = karma - 1 WHERE word = %s"
                        )
                        cursor.execute(SQLRemoveKarma, (usuario.lower(),))
                        logger.info("Karma decreased for user", user=usuario.lower())

                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"-1 Karma para {usuario.lower()}",
                        message_thread_id=thread_id,
                    )
                    database.commit()
                    database.close()
                    karmaLimit[update.message.from_user.username] -= 1
                else:
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Non sexas tan egocéntrico tío",
                        message_thread_id=thread_id,
                    )
                    logger.warning(
                        "User tried to decrease their own karma",
                        user=update.message.from_user.username,
                    )
            else:
                if update.message.from_user.username not in karmaLimit:
                    karmaLimit[update.message.from_user.username] = 5

                if karmaLimit[update.message.from_user.username] == 0:
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Xa non podes asignar máis karma hoxe",
                        message_thread_id=thread_id,
                    )
                    logger.info(
                        "Karma limit reached", user=update.message.from_user.username
                    )
                    return

                database = mysql.connector.connect(
                    host=os.environ.get('MYSQL_HOST'),
                    user=os.environ.get('MYSQL_USER'),
                    password=os.environ.get('MYSQL_PASSWORD'),
                    database=os.environ.get('MYSQL_DATABASE'),
                )
                cursor = database.cursor()
                SQLUsers = "SELECT * FROM karma WHERE word = %s"
                cursor.execute(SQLUsers, (usuario.lower(),))
                usuarios = cursor.fetchall()

                if len(usuarios) == 0:
                    SQLCreateuser = (
                        "INSERT INTO karma (word, karma, is_user) VALUES (%s,-1, false)"
                    )
                    cursor.execute(SQLCreateuser, (usuario.lower(),))
                    logger.info(
                        "New word created in karma database with negative karma",
                        word=usuario.lower(),
                    )
                else:
                    SQLRemoveKarma = (
                        "UPDATE karma SET karma = karma - 1 WHERE word = %s"
                    )
                    cursor.execute(SQLRemoveKarma, (usuario.lower(),))
                    logger.info("Karma decreased for word", word=usuario.lower())

                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"-1 Karma a {usuario.lower()}",
                    message_thread_id=thread_id,
                )
                database.commit()
                database.close()
                karmaLimit[update.message.from_user.username] -= 1
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Necesito un usuario para asignarlle karma",
                message_thread_id=thread_id,
            )
            logger.warning(
                "Karma down command received without arguments",
                user_id=update.effective_user.id if update.effective_user else None,
            )


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
                host=os.environ.get('MYSQL_HOST'),
                user=os.environ.get('MYSQL_USER'),
                password=os.environ.get('MYSQL_PASSWORD'),
                database=os.environ.get('MYSQL_DATABASE'),
            )
            cursor = database.cursor()

            if usuario[0] == "@":
                usuario = usuario[1:]
                SQLUsers = "SELECT karma FROM karma WHERE word = %s"
                cursor.execute(SQLUsers, (usuario.lower(),))
                karma = cursor.fetchone()

                if karma is None:
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
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=f"El Karma de {usuario.lower()} es {karma}",
                        message_thread_id=thread_id,
                    )
                    logger.info("Displayed karma for user", user=usuario.lower())
            else:
                usuario = usuario[1:]
                SQLUsers = "SELECT karma FROM karma WHERE word = %s"
                cursor.execute(SQLUsers, (usuario.lower(),))
                karma = cursor.fetchone()

                if karma is None:
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
            host=os.environ.get('MYSQL_HOST'),
            user=os.environ.get('MYSQL_USER'),
            password=os.environ.get('MYSQL_PASSWORD'),
            database=os.environ.get('MYSQL_DATABASE'),
        )
        cursor = database.cursor()

        SQLPrimeros = "SELECT word, karma FROM karma WHERE is_user = true ORDER BY karma DESC LIMIT 3"
        cursor.execute(SQLPrimeros)
        users = cursor.fetchall()

        for user in users:
            word, karma = user  # Correctly unpack the tuple
            karma_list += f"{word} - {karma}\n"
        logger.info("Top users with karma retrieved", users=users)

        karma_list += "\nPalabras con más karma:\n\n"
        SQLPrimerosPalabras = "SELECT word, karma FROM karma WHERE is_user = false ORDER BY karma DESC LIMIT 3"
        cursor.execute(SQLPrimerosPalabras)
        words = cursor.fetchall()

        for word in words:
            word_text, karma = word  # Correctly unpack the tuple
            karma_list += f"{word_text} - {karma}\n"
        logger.info("Top words with karma retrieved", words=words)

        karma_list += "\nUsuarios con menos karma:\n\n"
        SQLUltimos = "SELECT word, karma FROM karma WHERE is_user = true ORDER BY karma ASC LIMIT 3"
        cursor.execute(SQLUltimos)
        users = cursor.fetchall()

        for user in users:
            word, karma = user  # Correctly unpack the tuple
            karma_list += f"{word} - {karma}\n"
        logger.info("Bottom users with karma retrieved", users=users)

        karma_list += "\nPalabras con menos karma:\n\n"
        SQLUltimasPalabras = "SELECT word, karma FROM karma WHERE is_user = false ORDER BY karma ASC LIMIT 3"
        cursor.execute(SQLUltimasPalabras)
        words = cursor.fetchall()

        for word in words:
            word_text, karma = word  # Correctly unpack the tuple
            karma_list += f"{word_text} - {karma}\n"
        logger.info("Bottom words with karma retrieved", words=words)

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=karma_list,
            message_thread_id=thread_id,
        )
        database.close()
