from telegram import Update
from telegram.ext import ContextTypes
import os
import mysql.connector


connection_pool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name="my_pool",
        pool_size=5,
        pool_reset_session=True,
        host=os.environ.get('MYSQL_HOST'),
        user=os.environ.get('MYSQL_USER'),
        password=os.environ.get('MYSQL_PASSWORD'),
        database=os.environ.get('MYSQL_DATABASE'),
    )

async def add_quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global connection_pool
    thread_id = update.message.message_thread_id
    quoted_msg = update.effective_message.reply_to_message
    print(quoted_msg.text)
    print(quoted_msg.from_user.username)
    database = connection_pool.get_connection()
    cursor = database.cursor()
    SQLCheckQuote = "SELECT * FROM quotes WHERE quote = %s"
    cursor.execute(SQLCheckQuote, (quoted_msg.text,))
    quotes = cursor.fetchall()
    if len(quotes) == 0:
        if quoted_msg.from_user.username is not None:
            SQLAddQuote="INSERT INTO quotes (quote, user) VALUES (%s,%s)"
            cursor.execute(SQLAddQuote, (quoted_msg.text,quoted_msg.from_user.username))
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Cita agregada", message_thread_id=thread_id)
            database.commit()
            database.close()
            return
        else:
            SQLAddQuote="INSERT INTO quotes (quote, user) VALUES (%s,%s)"
            cursor.execute(SQLAddQuote, (quoted_msg.text,"Anonimous"))
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Cita agregada", message_thread_id=thread_id)
            database.commit()
            database.close()
            return
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Xa existe a cita", message_thread_id=thread_id)