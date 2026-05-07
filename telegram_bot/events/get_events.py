import os

import requests

from telegram_bot.utils.logger import logger

EVENTBRITE_API = "https://www.eventbriteapi.com/v3"


def get_next_event() -> dict | None:
    organization_id = os.environ.get("EVENTBRITE_ORGANIZATION_ID")
    token = os.environ.get("EVENTBRITE_TOKEN")
    if not organization_id or not token:
        logger.error("Eventbrite configuration is missing")
        return None

    try:
        response = requests.get(
            f"{EVENTBRITE_API}/organizations/{organization_id}/events/",
            headers={"Authorization": f"Bearer {token}"},
            params={"time_filter": "current_future"},
            timeout=10,
        )
        logger.debug("Eventbrite request completed", url=response.url)
        response.raise_for_status()
        events_result = response.json()
    except (requests.RequestException, ValueError) as error:
        logger.error("Error retrieving events", error=str(error))
        return None

    events = events_result.get("events", [])
    if not events:
        logger.info("No future Eventbrite events found")
        return {}

    return events[0]
