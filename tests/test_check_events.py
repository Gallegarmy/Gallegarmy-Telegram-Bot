import pytest
from telegram_bot.events.check_coruna_event import check_event
from telegram_bot.events.check_events_city import check_event_city, check_repeated_event


def make_event(name: str, month: int = 6) -> dict:
    return {
        "name": {"text": name},
        "start": {"local": f"2026-{month:02d}-15T18:00:00"},
        "url": "https://example.com/event",
    }


# --- check_event ---

def test_check_event_single_event_returns_it():
    event = make_event("Only Event")
    assert check_event([event]) == event


def test_check_event_different_names_returns_first():
    first = make_event("Admin Coruña")
    second = make_event("Olivarmy Vigo")
    assert check_event([first, second]) == first


def test_check_event_same_name_same_month_returns_second():
    first = make_event("SysArmy Galicia", month=6)
    second = make_event("SysArmy Galicia", month=6)
    assert check_event([first, second]) == second


def test_check_event_same_name_different_month_returns_first():
    first = make_event("SysArmy Galicia", month=6)
    second = make_event("SysArmy Galicia", month=7)
    assert check_event([first, second]) == first


def test_check_event_name_comparison_is_case_insensitive():
    first = make_event("SYSARMY GALICIA", month=6)
    second = make_event("sysarmy galicia", month=6)
    # Same name (after strip/lower), same month → returns second
    assert check_event([first, second]) == second


# --- check_repeated_event ---

def test_check_repeated_event_different_names_returns_current():
    current = make_event("Admin Coruña")
    next_ev = make_event("Olivarmy Vigo")
    assert check_repeated_event(current, next_ev) == current


def test_check_repeated_event_same_name_same_month_returns_next():
    current = make_event("SysArmy", month=6)
    next_ev = make_event("SysArmy", month=6)
    assert check_repeated_event(current, next_ev) == next_ev


def test_check_repeated_event_same_name_different_month_returns_current():
    current = make_event("SysArmy", month=6)
    next_ev = make_event("SysArmy", month=7)
    assert check_repeated_event(current, next_ev) == current


# --- check_event_city ---

def test_check_event_city_single_event_returns_it():
    event = make_event("Admin Coruña")
    assert check_event_city([event], "coruna") == event


def test_check_event_city_coruna_matches_admin_keyword():
    coruna = make_event("Admin Coruña", month=6)
    next_ev = make_event("Admin Coruña", month=7)
    result = check_event_city([coruna, next_ev], "coruna")
    # Different months → check_repeated_event returns current (coruna)
    assert result == coruna


def test_check_event_city_vigo_matches_olivarmy_keyword():
    vigo = make_event("Olivarmy Vigo", month=6)
    next_ev = make_event("Olivarmy Vigo", month=6)
    result = check_event_city([vigo, next_ev], "vigo")
    # Same name, same month → check_repeated_event returns next
    assert result == next_ev


def test_check_event_city_no_match_returns_no_event_string():
    first = make_event("Random Event")
    second = make_event("Another Event")
    assert check_event_city([first, second], "coruna") == "No event"


def test_check_event_city_unknown_city_returns_no_event_string():
    first = make_event("Admin Event")
    second = make_event("Next Event")
    assert check_event_city([first, second], "madrid") == "No event"
