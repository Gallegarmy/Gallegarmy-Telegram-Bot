from telegram import Update
from telegram.ext import ContextTypes
from datetime import timedelta, datetime
import structlog
import os, requests
from datetime import datetime
from datetime import timezone



logger = structlog.get_logger()


EVENTBRITE_API = os.environ["EVENTBRITE_API"]
EVENTBRITE_ORGANIZATION_ID = os.environ["EVENTBRITE_ORGANIZATION_ID"]
EVENTBRITE_TOKEN = os.environ["EVENTBRITE_TOKEN"]

def get_next_event() -> dict:
    response = requests.get(f'https://www.eventbriteapi.com/v3/organizations/{EVENTBRITE_ORGANIZATION_ID}/events/?time_filter=current_future', headers={'Authorization': f'Bearer {EVENTBRITE_TOKEN}'})
    logger.debug(f"Request URL: {response.url}")
    if response.status_code == 200:
        events_result = response.json()
        events = events_result.get('events', [])
        event = events[0]
    else:
        logger.error(f"Error retrieving events: {response.status_code} - {response.text}")
        event = {}
    return event

async def events(update: Update, context: ContextTypes.DEFAULT_TYPE):
    thread_id = update.message.message_thread_id if update.message else None
    logger.info(
        "Events command received",
        user_id=update.effective_user.id if update.effective_user else None,
        chat_id=update.effective_chat.id if update.effective_chat else None,
    )

    event = get_next_event()
        
    if event:
            
            start_time = str(event['start'].get('local'))
            dt = datetime.fromisoformat(start_time)
            event_time = dt.strftime("%d/%m %H:%M")
            event_message = (
                f"Próximo evento de Sysarmy Galicia:\n\n"
                f"{event['name'].get('text')}\n\n"
                f"Fecha y Hora: {event_time}\n\n"
                f"Meetup: '{event['url']}'\n\n"
            )
            if update.effective_chat:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=event_message,
                    message_thread_id=thread_id,
                )
                logger.info(
                    "Event message sent", chat_id=update.effective_chat.id, thread_id=thread_id
                )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Ocorreu un erro, contacte ao seu Sysadmin mais próximo",
            message_thread_id=thread_id,
        )
    

