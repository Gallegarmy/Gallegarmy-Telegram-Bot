import datetime, sqlite3
from datetime import datetime, date
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler


async def kup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    thread_id = update.message.message_thread_id
    if context.args:
        usuario = str(context.args[0])
        if usuario[0] != "@":
            await context.bot.send_message(chat_id=update.effective_chat.id, text='É mellor agregar usuarios con @ para non cometer erros de tipeo :)', message_thread_id=thread_id)
        else:
            usuario = usuario[1::]
            database = sqlite3.connect('sqlite.db')
            cursor = database.cursor()
            SQLUsers = ("SELECT * FROM karma WHERE user = ?")
            cursor.execute(SQLUsers, (usuario,))
            usuarios = cursor.fetchall()
            if len(usuario) == 0:
                SQLCreateuser = ("INSERT INTO karma (user, karma) VALUES (? , 1)")
                cursor.execute(SQLCreateuser, (usuario,))
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f'+1 Karma para {usuario}', message_thread_id=thread_id)
            else:
                SQLAddKarma = ("UPDATE karma SET karma = karma + 1 WHERE user = ?")
                cursor.execute(SQLAddKarma, (usuario,))
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f'+1 Karma para {usuario}', message_thread_id=thread_id)
            database.commit()
            database.close()
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Necesito un usuario para asignarlle karma', message_thread_id=thread_id)