from telegram_bot.db.db_handler import DbHandler
import structlog

logger = structlog.get_logger()


def updatedb_karma(target_user: str, karma_op: int, is_user: bool=False) -> None:
    database = DbHandler()
    try:
        database.connect()
        sentence = r"SELECT word FROM karma WHERE word = %s LIMIT 1"
        cursor = database.execute(sentence, params=(target_user,))
        result = cursor.fetchone()
        exists = result is not None and len(result) > 0

        if exists:
            sentence = r"UPDATE karma SET karma = karma + %s WHERE word = %s"
            params = (karma_op, target_user)
        else:
            sentence = r"INSERT INTO karma (karma, word, is_user) VALUES (%s, %s, %s)"
            params = (karma_op, target_user, is_user)

        cursor = database.execute(sentence, params=params)
        database.commit()
        return cursor.fetchone()
    except Exception as error:
        logger.error(error)
    finally:
        database.close()


def getdb_top3() -> None:
    sentence = r"SELECT word, karma FROM karma WHERE is_user = true ORDER BY karma DESC LIMIT 3"
    try:
        database = DbHandler()
        database.connect()
        cursor = database.execute(sentence, params=())
        return cursor.fetchall() or tuple()
    except Exception as error:
        logger.error(error)
    finally:
        database.close()

def getdb_last3() -> None:
    sentence = r"SELECT word, karma FROM karma WHERE is_user = true ORDER BY karma ASC LIMIT 3"
    try:
        database = DbHandler()
        database.connect()
        cursor = database.execute(sentence, params=())
        return cursor.fetchall() or tuple()
    except Exception as error:
        logger.error(error)
    finally:
        database.close()

def getdb_user_karma(user: str) -> None:
    try:
        sentence = r"SELECT karma FROM karma WHERE word = %s"
        database = DbHandler()
        database.connect()
        cursor = database.execute(sentence, (user,))
        result = cursor.fetchone()
        if result is None:
            result = 0
        else:
            result = result.get('karma')
        return result
    except Exception as error:
        logger.error(error)
    finally:
        database.close()







