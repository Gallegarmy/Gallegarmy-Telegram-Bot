from telegram import Update
from telegram.ext import ContextTypes
import sqlite3
from datetime import timedelta, datetime


def first_friday_of_month(year, month):
    current_date = datetime(year, month, 1)
    first_day_of_month = current_date.weekday()
    offset_to_friday = (4 - first_day_of_month) % 7
    first_friday_date = current_date + timedelta(days=offset_to_friday)
    return first_friday_date


async def cerveza(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get current year and month
    current_year = datetime.now().year
    current_month = datetime.now().month
    thread_id = update.message.message_thread_id
    if datetime.now() > first_friday_of_month(current_year, current_month):
        next_month_year = current_year if current_month < 12 else current_year + 1
        next_month = current_month + 1 if current_month < 12 else 1
        database = sqlite3.connect("sqlite.db")
        cursor = database.cursor()
        SQLEvents = "SELECT * FROM events WHERE fecha = ?"
        formatted_date = first_friday_of_month(next_month_year, next_month).strftime(
            "%d-%m-%Y"
        )
        cursor.execute(SQLEvents, (formatted_date,))
        event = cursor.fetchone()
        if event is None:
            SQLCreateEvent = "INSERT INTO events (fecha, hora, link, lugar, maps) VALUES (? , '19:00', 'https://www.meetup.com/es-ES/gallegarmy/', 'Fire Capitano (Rúa Federico García, 2, 15009 A Coruña)', 'https://maps.app.goo.gl/ao8dejkwv74QV6eb7')"
            cursor.execute(SQLCreateEvent, (formatted_date,))
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Próximo evento de Admin Cañas:\n\nFecha: {first_friday_of_month(next_month_year, next_month).strftime('%d-%m-%Y')}\n\nHora: 19:00\n\nMeetup: https://www.meetup.com/es-ES/gallegarmy/events/300259426/\n\nUbicación: Fire Capitano (Rúa Federico García, 2, 15009 A Coruña) \n\nhttps://maps.app.goo.gl/ao8dejkwv74QV6eb7",
                message_thread_id=thread_id,
            )
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Próximo evento de Admin Cañas:\n\nFecha: {event[0]}\n\nHora: {event[1]}\n\nMeetup: {event[2]}\n\nUbicación: {event[3]}\n\n{event[4]}",
                message_thread_id=thread_id,
            )
        database.commit()
        database.close()
    else:
        database = sqlite3.connect("sqlite.db")
        cursor = database.cursor()
        SQLEvents = "SELECT * FROM events WHERE fecha = ?"
        formatted_date = first_friday_of_month(current_year, current_month).strftime(
            "%d-%m-%Y"
        )
        cursor.execute(SQLEvents, (formatted_date,))
        event = cursor.fetchone()
        if event is None:
            SQLCreateEvent = "INSERT INTO events (fecha, hora, link, lugar, maps) VALUES (? , '19:00', 'https://www.meetup.com/es-ES/gallegarmy/', 'Fire Capitano (Rúa Federico García, 2, 15009 A Coruña)', 'https://maps.app.goo.gl/ao8dejkwv74QV6eb7')"
            cursor.execute(SQLCreateEvent, (formatted_date,))
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Próximo evento de Admin Cañas:\n\nFecha: {first_friday_of_month(next_month_year, next_month).strftime('%d-%m-%Y')}\n\nHora: 19:00\n\nMeetup: https://www.meetup.com/es-ES/gallegarmy/events/300259426/\n\nUbicación: Fire Capitano (Rúa Federico García, 2, 15009 A Coruña) \n\nhttps://maps.app.goo.gl/ao8dejkwv74QV6eb7",
                message_thread_id=thread_id,
            )
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Próximo evento de Admin Cañas:\n\nFecha: {event[0]}\n\nHora: {event[1]}\n\nMeetup: {event[2]}\n\nUbicación: {event[3]}\n\n{event[4]}",
                message_thread_id=thread_id,
            )
        database.commit()
        database.close()


async def cervezahora(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admins = [line.strip() for line in open("admins.txt")]
    thread_id = update.message.message_thread_id
    if context.args:
        fecha = context.args[0]
        hora = context.args[1]
        if str(update.message.from_user.username) in admins:
            database = sqlite3.connect("sqlite.db")
            cursor = database.cursor()
            SQLEvents = "UPDATE events SET hora = ? WHERE fecha = ?"
            cursor.execute(SQLEvents, (hora, fecha))
            database.commit()
            database.close()
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Se ha modificado la hora del evento",
                message_thread_id=thread_id,
            )


async def cervezalugar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admins = [line.strip() for line in open("admins.txt")]
    thread_id = update.message.message_thread_id
    if context.args:
        fecha = context.args[0]
        lugar = context.args[1]
        if str(update.message.from_user.username) in admins:
            database = sqlite3.connect("sqlite.db")
            cursor = database.cursor()
            SQLEvents = "UPDATE events SET lugar = ? WHERE fecha = ?"
            cursor.execute(SQLEvents, (lugar, fecha))
            database.commit()
            database.close()
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Se ha modificado el lugar del evento",
                message_thread_id=thread_id,
            )


async def cervezamapa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admins = [line.strip() for line in open("admins.txt")]
    thread_id = update.message.message_thread_id
    if context.args:
        fecha = context.args[0]
        mapa = context.args[1]
        if str(update.message.from_user.username) in admins:
            database = sqlite3.connect("sqlite.db")
            cursor = database.cursor()
            SQLEvents = "UPDATE events SET maps = ? WHERE fecha = ?"
            cursor.execute(SQLEvents, (mapa, fecha))
            database.commit()
            database.close()
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Se ha modificado el mapa del evento",
                message_thread_id=thread_id,
            )


async def cervezaasistencia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admins = [line.strip() for line in open("admins.txt")]
    thread_id = update.message.message_thread_id
    if context.args:
        fecha = context.args[0]
        asistentes = int(context.args[1])
        if str(update.message.from_user.username) in admins:
            database = sqlite3.connect("sqlite.db")
            cursor = database.cursor()
            SQLEvents = "UPDATE events SET asistentes = ? WHERE fecha = ?"
            cursor.execute(SQLEvents, (asistentes, fecha))
            database.commit()
            database.close()
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Se ha modificado la asistencia del evento",
                message_thread_id=thread_id,
            )


async def cervezalink(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admins = [line.strip() for line in open("admins.txt")]
    thread_id = update.message.message_thread_id
    if context.args:
        fecha = context.args[0]
        link = context.args[1]
        if str(update.message.from_user.username) in admins:
            database = sqlite3.connect("sqlite.db")
            cursor = database.cursor()
            SQLEvents = "UPDATE events SET link = ? WHERE fecha = ?"
            cursor.execute(SQLEvents, (link, fecha))
            database.commit()
            database.close()
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Se ha modificado la asistencia del evento",
                message_thread_id=thread_id,
            )
