from telegram import Update
from telegram.ext import ContextTypes
import os
import mysql.connector



async def add_quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    thread_id = update.message.message_thread_id
    quoted_msg = update.effective_message.reply_to_message
    if quoted_msg is None:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Necesítase unha mensaxe para citar.", message_thread_id=thread_id if thread_id else None)
        return    
    database = mysql.connector.connect(
                host=os.environ.get('MYSQL_HOST'),
                user=os.environ.get('MYSQL_USER'),
                password=os.environ.get('MYSQL_PASSWORD'),
                database=os.environ.get('MYSQL_DATABASE'),
    )
    cursor = database.cursor()
    SQLCheckQuote = "SELECT * FROM quotes WHERE quote = %s"
    cursor.execute(SQLCheckQuote, (quoted_msg.text,))
    quotes = cursor.fetchall()
       
    if len(quotes) == 0:
        if quoted_msg.from_user.username is not None:
            SQLAddQuote="INSERT INTO quotes (quote, user) VALUES (%s,%s)"
            cursor.execute(SQLAddQuote, (quoted_msg.text,quoted_msg.from_user.username))
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Cita agregada.", message_thread_id=thread_id if thread_id else None)
            database.commit()
            database.close()
            return
        else:
            SQLAddQuote="INSERT INTO quotes (quote, user) VALUES (%s,%s)"
            cursor.execute(SQLAddQuote, (quoted_msg.text,"Anonimous"))
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Cita agregada.", message_thread_id=thread_id if thread_id else None)
            database.commit()
            database.close()
            return
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Xa existe a cita.", message_thread_id=thread_id if thread_id else None)


async def random_quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global connection
    thread_id = update.message.message_thread_id
    database = mysql.connector.connect(
                host=os.environ.get('MYSQL_HOST'),
                user=os.environ.get('MYSQL_USER'),
                password=os.environ.get('MYSQL_PASSWORD'),
                database=os.environ.get('MYSQL_DATABASE'),
    )
    cursor = database.cursor()
    if len(context.args) == 1:
        user = context.args[0]
        if user[0] == "@":
            user = user[1::]
        SQLSearchUserQuote="SELECT quote FROM quotes WHERE user = %s  ORDER BY RAND ( )  LIMIT 3"
        cursor.execute(SQLSearchUserQuote, (str(user),))
        quotes = cursor.fetchall()
        if len(quotes) > 0:
            user_quotes=f"Quotes ao azar de {user}:"
            for quote in quotes:
                user_quotes+=f"\n{quote[0]}"
            await context.bot.send_message(chat_id=update.effective_chat.id, text=user_quotes, message_thread_id=thread_id if thread_id else None)
            database.close()
            return
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Non se atoparon quotes dese usuario", message_thread_id=thread_id if thread_id else None)
            database.close()
            return
    elif len(context.args) < 1:
        SQLSearchRandomQuote="SELECT quote,user FROM quotes ORDER BY RAND ( )  LIMIT 1"
        cursor.execute(SQLSearchRandomQuote)
        result = cursor.fetchone()
        quote,user = result
        random_quote=f"Quote ao azar de Sysarmy Galicia:\nAutor {user}: {quote}"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=random_quote, message_thread_id=thread_id if thread_id else None)
        database.close()
        return
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Pasáronse máis argumentos dos permitidos", message_thread_id=thread_id if thread_id else None)
        database.close()
        return