from unittest.mock import MagicMock, patch

from telegram_bot.db.karma_facade import (
    getdb_last3,
    getdb_top3,
    getdb_user_karma,
    updatedb_karma,
)


def _mock_db(fetchone=None, fetchall=None):
    cursor = MagicMock()
    cursor.fetchone.return_value = fetchone
    cursor.fetchall.return_value = fetchall or []
    db = MagicMock()
    db.execute.return_value = cursor
    return db


# --- getdb_user_karma ---

def test_getdb_user_karma_unknown_user_returns_zero():
    db = _mock_db(fetchone=None)
    with patch("telegram_bot.db.karma_facade.DbHandler", return_value=db):
        assert getdb_user_karma("nobody") == 0


def test_getdb_user_karma_returns_stored_value():
    db = _mock_db(fetchone={"karma": 7})
    with patch("telegram_bot.db.karma_facade.DbHandler", return_value=db):
        assert getdb_user_karma("alice") == 7


def test_getdb_user_karma_null_karma_returns_zero():
    db = _mock_db(fetchone={"karma": None})
    with patch("telegram_bot.db.karma_facade.DbHandler", return_value=db):
        assert getdb_user_karma("alice") == 0


def test_getdb_user_karma_closes_connection_on_success():
    db = _mock_db(fetchone={"karma": 3})
    with patch("telegram_bot.db.karma_facade.DbHandler", return_value=db):
        getdb_user_karma("alice")
    db.close.assert_called_once()


def test_getdb_user_karma_closes_connection_on_error():
    db = MagicMock()
    db.connect.side_effect = RuntimeError("db down")
    with patch("telegram_bot.db.karma_facade.DbHandler", return_value=db):
        result = getdb_user_karma("alice")
    assert result == 0
    db.close.assert_called_once()


# --- getdb_top3 ---

def test_getdb_top3_returns_rows():
    rows = [{"word": "alice", "karma": 10}, {"word": "bob", "karma": 5}]
    db = _mock_db(fetchall=rows)
    with patch("telegram_bot.db.karma_facade.DbHandler", return_value=db):
        result = getdb_top3()
    assert result == rows


def test_getdb_top3_returns_empty_tuple_when_no_results():
    db = _mock_db(fetchall=None)
    db.execute.return_value.fetchall.return_value = None
    with patch("telegram_bot.db.karma_facade.DbHandler", return_value=db):
        result = getdb_top3()
    assert result == tuple() or result == []


# --- getdb_last3 ---

def test_getdb_last3_returns_rows():
    rows = [{"word": "carol", "karma": -5}]
    db = _mock_db(fetchall=rows)
    with patch("telegram_bot.db.karma_facade.DbHandler", return_value=db):
        result = getdb_last3()
    assert result == rows


# --- updatedb_karma ---

def test_updatedb_karma_inserts_new_user():
    cursor = MagicMock()
    cursor.fetchone.return_value = None  # User not found on SELECT
    db = MagicMock()
    db.execute.return_value = cursor

    with patch("telegram_bot.db.karma_facade.DbHandler", return_value=db):
        updatedb_karma("newuser", 1, True)

    assert db.execute.call_count == 2
    db.commit.assert_called_once()


def test_updatedb_karma_updates_existing_user():
    cursor = MagicMock()
    cursor.fetchone.return_value = {"word": "alice"}  # User exists
    db = MagicMock()
    db.execute.return_value = cursor

    with patch("telegram_bot.db.karma_facade.DbHandler", return_value=db):
        updatedb_karma("alice", 1)

    update_call = db.execute.call_args_list[1]
    assert "UPDATE" in update_call.args[0]
    db.commit.assert_called_once()


def test_updatedb_karma_closes_connection():
    cursor = MagicMock()
    cursor.fetchone.return_value = None
    db = MagicMock()
    db.execute.return_value = cursor

    with patch("telegram_bot.db.karma_facade.DbHandler", return_value=db):
        updatedb_karma("user", -1)

    db.close.assert_called_once()
