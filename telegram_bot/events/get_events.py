import os, requests
from telegram_bot.utils.logger import logger

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