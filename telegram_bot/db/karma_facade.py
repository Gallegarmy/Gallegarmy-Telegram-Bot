from telegram_bot.db.db_handler import DbHandler


def update_karma(target_user: str, karma_op: int, is_user: bool=False) -> None:
    database = DbHandler()
    try:
        database.connect()
        sentence = r"SELECT word FROM karma WHERE word = %s LIMIT 1"
        cursor = database.execute(sentence, params=(target_user,))
        result = cursor.fetchone()
        exists = result is not None and len(result) > 0

        if exists:
            sentence = r"UPDATE karma SET karma = karma + %s WHERE word = %s"
        else:
            sentence = r"INSERT INTO karma (karma, word, is_user) VALUES (%s, %s, %s)"

        cursor = database.execute(sentence, params=(karma_op, target_user, is_user))
        database.commit()
    except Exception as error:
        print(error)
    finally:
        database.close()












