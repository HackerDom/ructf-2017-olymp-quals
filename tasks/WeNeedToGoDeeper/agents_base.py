import sqlite3
from contextlib import contextmanager


@contextmanager
def db_connection():
    conn = sqlite3.connect('user_agents.db')
    try:
        cursor = conn.cursor()
        cursor\
            .execute(
             '''CREATE TABLE IF NOT EXISTS agents (user_agent text unique)''')
        yield cursor
    except sqlite3.IntegrityError:
        pass
    finally:
        conn.commit()
        conn.close()


def add_user_agent(user_agent):
    with db_connection() as cursor:
        cursor.execute(
            'INSERT INTO agents VALUES (?)', (user_agent,)
        )


def check_user_agents(user_agent):
    with db_connection() as cursor:
        cursor.execute(
            'SELECT * FROM agents WHERE user_agent=?', (user_agent,)
        )
        return cursor.fetchone() is not None
