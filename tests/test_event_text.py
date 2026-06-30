from telegram_bot.events.event_text import create_message_text


def test_message_contains_event_name():
    text = create_message_text("SysArmy Talk", "15/06", "19:00", "https://example.com")
    assert "SysArmy Talk" in text


def test_message_contains_date_and_time():
    text = create_message_text("Some Event", "20/07", "18:30", "https://example.com")
    assert "20/07" in text
    assert "18:30" in text


def test_message_contains_link():
    link = "https://eventbrite.com/e/12345"
    text = create_message_text("Event", "01/01", "10:00", link)
    assert link in text


def test_message_returns_string():
    result = create_message_text("Event", "01/01", "10:00", "https://example.com")
    assert isinstance(result, str)
