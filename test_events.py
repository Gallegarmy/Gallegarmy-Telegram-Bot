from datetime import datetime, timedelta

from telegram_bot.events.get_events import get_next_event


class FakeResponse:
    url = "https://example.test/events"

    def __init__(self, payload, status_code=200):
        self.payload = payload
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError("request failed")

    def json(self):
        return self.payload


def test_get_next_event_status_code_200(monkeypatch):
    future_date = (datetime.now() + timedelta(days=1)).isoformat()

    def fake_get(*args, **kwargs):
        return FakeResponse({"events": [{"start": {"local": future_date}}]})

    monkeypatch.setenv("EVENTBRITE_ORGANIZATION_ID", "2454750791881")
    monkeypatch.setenv("EVENTBRITE_TOKEN", "token")
    monkeypatch.setattr("telegram_bot.events.get_events.requests.get", fake_get)

    event = get_next_event()

    assert event is not None, "Expected a valid event dictionary."
    assert isinstance(event, dict), "Expected event to be a dictionary."


def test_get_next_event_start_in_future(monkeypatch):
    future_date = (datetime.now() + timedelta(days=1)).isoformat()

    def fake_get(*args, **kwargs):
        return FakeResponse({"events": [{"start": {"local": future_date}}]})

    monkeypatch.setenv("EVENTBRITE_ORGANIZATION_ID", "2454750791881")
    monkeypatch.setenv("EVENTBRITE_TOKEN", "token")
    monkeypatch.setattr("telegram_bot.events.get_events.requests.get", fake_get)

    event = get_next_event()

    event_start_time = event["start"].get("local")
    assert event_start_time is not None, "Expected a 'local' start time."
    event_start_datetime = datetime.fromisoformat(event_start_time)
    assert (
        event_start_datetime > datetime.now()
    ), "Expected the event start time to be in the future."


def test_get_next_event_returns_empty_dict_without_config(monkeypatch):
    monkeypatch.delenv("EVENTBRITE_ORGANIZATION_ID", raising=False)
    monkeypatch.delenv("EVENTBRITE_TOKEN", raising=False)

    assert get_next_event() == {}
