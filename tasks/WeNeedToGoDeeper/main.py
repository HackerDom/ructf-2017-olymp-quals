from flask import Flask, request
from hashlib import sha1  # so insecure
from agents_base import add_user_agent, check_user_agents


app = Flask(__name__)

SALT = "so salty, so cute:3 (RuCTF 2017) #ructf2017"
STARTING_STRING = '''
do you know that md5 of "ructf2017" is f94f38ab82c48353773b316a7a663e21?
'''

FLAG = "RuCTF:HarderBetterFasterStronger_Agent_2017"


@app.route("/")
def root_router():
    return "Srsly?!", "200 goto root plus {}"\
        .format(sha1(STARTING_STRING.encode()).hexdigest())


@app.route("/<some_hash>")
def task_router(some_hash):
    user_agent = str(request.user_agent)

    # fix little and big user agents
    if user_agent == "" or len(user_agent) > 512:
        user_agent = "0orTooBig"
    # fix all browser, lol
    if "Mozilla" in user_agent or "Opera" in user_agent:
        return "Your browser is banned!", "403 banned"

    # fix snakes
    if "python" in user_agent.lower():
        return "S-s-s-sssnakeee is here", "403 Python also banned!"

    # fix old user agents
    if check_user_agents(user_agent):
        return "Your have been banned!", "403 Banned"
    else:
        add_user_agent(user_agent)

    # ok, flag
    if some_hash == "acab4de47c6e35f6dab7f9ee17fae17858c14f3d":
        return "Find the flag, (or me, lol)",\
               "200 {}".format(FLAG)
    return "Yep! You're on the right way!", "200 goto root plus {}"\
        .format(sha1((some_hash + SALT).encode()).hexdigest())

"""
def gen_last_hash():
    answer, code = root_router()
    hashes = code.split()[-1]
    for _ in range(99):
        answer, hashes = task_router(hashes)
        hashes = hashes.split()[-1]
    print(hashes)
"""


if __name__ == '__main__':
    #gen_result()
    app.run("0.0.0.0", port=8080)
