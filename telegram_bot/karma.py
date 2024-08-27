import sqlite3
from telegram import Update
from telegram.ext import ContextTypes
from collections import defaultdict
import datetime

karmaLimit = defaultdict(int)
last_cleared_date = None


def initialize_db():
    database = sqlite3.connect("/app/sqlite.db")
    cursor = database.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS karma (
            user TEXT PRIMARY KEY,
            karma INTEGER DEFAULT 0
        )
    ''')
    database.commit()
    database.close()

async def kup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global karmaLimit, last_cleared_date
    now = datetime.datetime.now()
    if last_cleared_date is None or now.date() > last_cleared_date:
            karmaLimit.clear()
            last_cleared_date = now.date()
    if update.message and update.message.from_user and update.effective_chat:
        thread_id = update.message.message_thread_id
        if context.args:
            usuario = str(context.args[0])
            if usuario[0] == "@":
                usuario = usuario[1:]
            if usuario.lower() != str(update.message.from_user.username).lower():
                if update.message.from_user.username not in karmaLimit:
                    karmaLimit[update.message.from_user.username] = 5
                if karmaLimit[update.message.from_user.username] == 0:
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Xa non podes asignar máis karma hoxe",
                        message_thread_id=thread_id,
                    )
                    return
                
                database = sqlite3.connect("/app/sqlite.db")
                cursor = database.cursor()
                SQLUsers = "SELECT * FROM karma WHERE user = ?"
                cursor.execute(SQLUsers, (usuario.lower(),))
                usuarios = cursor.fetchall()
                if len(usuarios) == 0:
                    SQLCreateuser = "INSERT INTO karma (user, karma) VALUES (? , 1)"
                    cursor.execute(SQLCreateuser, (usuario.lower(),))
                else:
                    SQLAddKarma = "UPDATE karma SET karma = karma + 1 WHERE user = ?"
                    cursor.execute(SQLAddKarma, (usuario.lower(),))
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
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Necesito un usuario para asignarlle karma",
                message_thread_id=thread_id,
            )


async def kdown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global karmaLimit, last_cleared_date
    now = datetime.datetime.now()
    if last_cleared_date is None or now.date() > last_cleared_date:
            karmaLimit.clear()
            last_cleared_date = now.date()
    if update.message and update.message.from_user and update.effective_chat:
        thread_id = update.message.message_thread_id
        if context.args:
            usuario = str(context.args[0])
            if usuario[0] == "@":
                usuario = usuario[1:]
            if usuario.lower() != str(update.message.from_user.username).lower():
                if update.message.from_user.username not in karmaLimit:
                    karmaLimit[update.message.from_user.username] = 5
                if karmaLimit[update.message.from_user.username] == 0:
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text="Xa non podes asignar máis karma hoxe",
                        message_thread_id=thread_id,
                    )
                    return
                
                database = sqlite3.connect("/app/sqlite.db")
                cursor = database.cursor()
                SQLUsers = "SELECT * FROM karma WHERE user = ?"
                cursor.execute(SQLUsers, (usuario.lower(),))
                usuarios = cursor.fetchall()
                if len(usuarios) == 0:
                    SQLCreateuser = "INSERT INTO karma (user, karma) VALUES (? , -1)"
                    cursor.execute(SQLCreateuser, (usuario.lower(),))
                else:
                    SQLRemoveKarma = "UPDATE karma SET karma = karma - 1 WHERE user = ?"
                    cursor.execute(SQLRemoveKarma, (usuario.lower(),))
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
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Necesito un usuario para asignarlle karma",
                message_thread_id=thread_id,
            )


async def kshow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.effective_chat:
        thread_id = update.message.message_thread_id
        if context.args:
            usuario = str(context.args[0])
            if usuario[0] == "@":
                usuario = usuario[1:]
            database = sqlite3.connect("/app/sqlite.db")
            cursor = database.cursor()
            SQLUsers = "SELECT * FROM karma WHERE user = ?"
            cursor.execute(SQLUsers, (usuario.lower(),))
            usuarios = cursor.fetchall()
            if len(usuarios) == 0:
                SQLCreateuser = "INSERT INTO karma (user, karma) VALUES (? , 0)"
                cursor.execute(SQLCreateuser, (usuario.lower(),))
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"El Karma de {usuario.lower()} es 0",
                    message_thread_id=thread_id,
                )
            else:
                SQLShowKarma = "SELECT karma FROM karma WHERE user = ?"
                cursor.execute(SQLShowKarma, (usuario.lower(),))
                karma = cursor.fetchone()
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=f"El Karma de {usuario.lower()} es {karma[0]}",
                    message_thread_id=thread_id,
                )
            database.commit()
            database.close()
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Necesito un usuario para mostrar o seu karma",
                message_thread_id=thread_id,
            )


async def klist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.effective_chat:
        thread_id = update.message.message_thread_id
        karma_list = "Usuarios con más karma:\n\n"
        database = sqlite3.connect("/app/sqlite.db")
        cursor = database.cursor()
        SQLPrimeros = "SELECT user, karma FROM karma ORDER BY karma DESC LIMIT 3"
        cursor.execute(SQLPrimeros)
        users = cursor.fetchall()
        for user in users:
            karma_list += f"{user[0]} - {user[1]}\n"
        karma_list += "\nUsuarios con menos karma:\n\n"
        SQLUltimos = "SELECT user, karma FROM karma ORDER BY karma ASC LIMIT 3"
        cursor.execute(SQLUltimos)
        users = cursor.fetchall()
        for user in users:
            karma_list += f"{user[0]} - {user[1]}\n"
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=karma_list,
            message_thread_id=thread_id,
        )
        database.close()
