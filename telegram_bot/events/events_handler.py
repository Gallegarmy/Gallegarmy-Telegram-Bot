from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime
from telegram_bot.utils.logger import logger
from .get_events import get_next_event
from .event_text import create_message_text
from ..utils.messaging import MessagingService



async def events(update: Update, context: ContextTypes.DEFAULT_TYPE):
    thread_id = update.message.message_thread_id if update.message else None
    chat_id = update.effective_chat.id if update.effective_chat else None
    logger.info(
        "Events command received",
        user_id=update.effective_user.id if update.effective_user else None,
        chat_id=update.effective_chat.id if update.effective_chat else None,
    )
    messaging = MessagingService(context.bot)
    event = get_next_event()
        
    if event:
            
            start_time = str(event['start'].get('local'))
            dt = datetime.fromisoformat(start_time)
            event_date = dt.strftime("%d/%m")
            event_time = dt.strftime("%H:%M")
            event_message = create_message_text(event['name'].get('text'),event_date, event_time, event['url'])
            if update.effective_chat:
                await messaging.send_message(chat_id,event_message,thread_id,)
                logger.info("Event message sent", chat_id=update.effective_chat.id, thread_id=thread_id)
    else:
        await messaging.send_message(
            chat_id=chat_id, text="Ocorreu un erro, contacte ao seu Sysadmin mais próximo", thread_id=thread_id,
        )