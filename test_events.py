import pytest
from unittest.mock import patch
from datetime import datetime, timedelta
import requests
import requests_mock

from telegram_bot.cerveza import get_next_event

# Check if get_next_event() returns a response with status code 200
def test_get_next_event_status_code_200():
    with requests_mock.Mocker() as mocker:
        mock_url = 'https://www.eventbriteapi.com/v3/organizations/2454750791881/events/?time_filter=current_future'
        mocker.get(mock_url, json={"events": [{"start": {"local": (datetime.now() + timedelta(days=1)).isoformat()}}]}, status_code=200)
        
        # Call the function
        event = get_next_event()
        
        # Assert that the event has been returned (not empty dict), indicating a successful response
        assert event is not None, "Expected a valid event dictionary."
        assert isinstance(event, dict), "Expected event to be a dictionary."
        
# Check if the event's 'local' start time is in the future
def test_get_next_event_start_in_future():
    with requests_mock.Mocker() as mocker:
        future_date = (datetime.now() + timedelta(days=1)).isoformat()
        mock_url = 'https://www.eventbriteapi.com/v3/organizations/2454750791881/events/?time_filter=current_future'
        mocker.get(mock_url, json={"events": [{"start": {"local": future_date}}]}, status_code=200)
        
        event = get_next_event()
        
        event_start_time = event['start'].get('local')
        assert event_start_time is not None, "Expected a 'local' start time."
        event_start_datetime = datetime.fromisoformat(event_start_time)
        assert event_start_datetime > datetime.now(), "Expected the event start time to be in the future."

