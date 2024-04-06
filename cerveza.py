from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import threading
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
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Próximo evento de Admin Cañas:\n\nFecha: {first_friday_of_month(next_month_year, next_month).strftime('%d-%m-%Y')}\n\nHora: 19:00\n\nUbicación: https://www.google.com/maps/place//data=!4m2!3m1!1s0xd2e7ca45763defb:0x6165fd3109dd362d?sa=X&ved=1t:8290&ictx=111", message_thread_id=thread_id)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Próximo evento de Admin Cañas:\n\nFecha: {first_friday_of_month(current_year, current_month).strftime('%d-%m-%Y')}\n\nHora: 19:00\n\nUbicación: https://www.google.com/maps/place//data=!4m2!3m1!1s0xd2e7ca45763defb:0x6165fd3109dd362d?sa=X&ved=1t:8290&ictx=111", message_thread_id=thread_id)