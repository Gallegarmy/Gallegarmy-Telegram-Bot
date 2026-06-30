import requests
from datetime import datetime, timedelta

from telegram_bot.events.get_events import get_next_event


class FakeResponse:
    url = "https://example.test/events"

    def __init__(self, payload, status_code=200):
        self.payload = payload
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(response=self)

    def json(self):
        return self.payload


def future_event(name="SysArmy Galicia", days=1):
    dt = (datetime.now() + timedelta(days=days)).isoformat()
    return {"name": {"text": name}, "start": {"local": dt}, "url": "https://example.com"}


def test_returns_none_without_env_config(monkeypatch):
    monkeypatch.delenv("EVENTBRITE_ORGANIZATION_ID", raising=False)
    monkeypatch.delenv("EVENTBRITE_TOKEN", raising=False)
    assert get_next_event() is None


def test_returns_empty_dict_when_no_events(monkeypatch):
    monkeypatch.setenv("EVENTBRITE_ORGANIZATION_ID", "123")
    monkeypatch.setenv("EVENTBRITE_TOKEN", "token")
    monkeypatch.setattr(
        "telegram_bot.events.get_events.requests.get",
        lambda *a, **kw: FakeResponse({"events": []}),
    )
    assert get_next_event() == {}


def test_returns_event_dict_on_success(monkeypatch):
    monkeypatch.setenv("EVENTBRITE_ORGANIZATION_ID", "123")
    monkeypatch.setenv("EVENTBRITE_TOKEN", "token")
    monkeypatch.setattr(
        "telegram_bot.events.get_events.requests.get",
        lambda *a, **kw: FakeResponse({"events": [future_event()]}),
    )
    result = get_next_event()
    assert isinstance(result, dict)
    assert "start" in result


def test_returns_none_on_http_error(monkeypatch):
    monkeypatch.setenv("EVENTBRITE_ORGANIZATION_ID", "123")
    monkeypatch.setenv("EVENTBRITE_TOKEN", "token")
    monkeypatch.setattr(
        "telegram_bot.events.get_events.requests.get",
        lambda *a, **kw: FakeResponse({}, status_code=401),
    )
    assert get_next_event() is None


def test_returns_none_on_network_error(monkeypatch):
    monkeypatch.setenv("EVENTBRITE_ORGANIZATION_ID", "123")
    monkeypatch.setenv("EVENTBRITE_TOKEN", "token")

    def raise_error(*a, **kw):
        raise requests.ConnectionError("network down")

    monkeypatch.setattr("telegram_bot.events.get_events.requests.get", raise_error)
    assert get_next_event() is None


def test_city_parameter_filters_by_vigo(monkeypatch):
    monkeypatch.setenv("EVENTBRITE_ORGANIZATION_ID", "123")
    monkeypatch.setenv("EVENTBRITE_TOKEN", "token")
    vigo = future_event("Olivarmy Vigo")
    next_ev = future_event("Olivarmy Vigo")
    monkeypatch.setattr(
        "telegram_bot.events.get_events.requests.get",
        lambda *a, **kw: FakeResponse({"events": [vigo, next_ev]}),
    )
    result = get_next_event(city="vigo")
    assert result is not None


def test_city_parameter_filters_by_coruna(monkeypatch):
    monkeypatch.setenv("EVENTBRITE_ORGANIZATION_ID", "123")
    monkeypatch.setenv("EVENTBRITE_TOKEN", "token")
    coruna = future_event("Admin Coruña")
    next_ev = future_event("Admin Coruña")
    monkeypatch.setattr(
        "telegram_bot.events.get_events.requests.get",
        lambda *a, **kw: FakeResponse({"events": [coruna, next_ev]}),
    )
    result = get_next_event(city="coruna")
    assert result is not None
