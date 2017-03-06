from flask import Flask, request
from hashlib import sha1  # so insecure
import sqlite3
from contextlib import contextmanager


app = Flask(__name__)

SALT = "so salty, so cute:3 (RuCTF 2017) #ructf2017"
STARTING_STRING = '''
do you know that md5 of "ructf2017" is f94f38ab82c48353773b316a7a663e21?
'''

FLAG = "RuCTF: HarderBetterFasterStrongerUserAgent2017"


@contextmanager
def db_connection():
    conn = sqlite3.connect('user_agents.db')
    try:
        cursor = conn.cursor()
        cursor\
            .execute(
             'CREATE TABLE IF NOT EXISTS agents (user_agent text unique)')
        yield cursor
    except sqlite3.IntegrityError:
        pass
    finally:
        conn.commit()
        conn.close()


def add_user_agent(user_agent):
    with db_connection() as cursor:
        cursor.execute(
            'INSERT INTO agents VALUES (?)', (user_agent,))


def check_user_agents(user_agent):
    with db_connection() as cursor:
        cursor.execute(
            'SELECT * FROM agents WHERE user_agent=?', (user_agent,))
        return cursor.fetchone() is not None


@app.route("/")
def root_router():
    return "Srly?! I hate guests, get out!", "200 go to root plus {}"\
        .format(sha1(STARTING_STRING.encode()).hexdigest())


@app.route("/<some_hash>")
def task_router(some_hash):
    user_agent = str(request.user_agent)

    # fix little and big user agents
    if user_agent == "" or len(user_agent) > 512:
        user_agent = "0orTooBig"
    # fix all browsers, lol
    if "Mozilla" in user_agent or "Opera" in user_agent:
        return "Your browser is banned!", "403 Browser is banned"

    # fix snakes
    if "python" in user_agent.lower():
        return "S-s-s-sssnakeee is here", "403 Python is banned also!"

    # fix old user agents
    if check_user_agents(user_agent):
        return "Your have been banned!", "403 Browser is Banned"
    else:
        add_user_agent(user_agent)

    # ok, flag
    if some_hash == "acab4de47c6e35f6dab7f9ee17fae17858c14f3d":
        return "Find the flag, (or me, lol)",\
               '200 {}'.format(FLAG)
    return "Yep! You're on the right way!", "200 goto root plus {}"\
        .format(sha1((some_hash + SALT).encode()).hexdigest())


if __name__ == '__main__':
    app.run("0.0.0.0", port=8080)
