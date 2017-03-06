from urllib.request import urlopen, Request
import sys


def get_next_hash(hash_str, const):
    new_request = Request(
        url="http://{}/".format(sys.argv[1]) + hash_str,
        headers={
            'User-Agent': "snake3.smth + {}".format(const)
        }
    )
    return urlopen(new_request).msg.split()[-1]


global_hash_sting = ""
i = 0
while "RuCTF" not in global_hash_sting:
    i += 1
    print(i, global_hash_sting)
    global_hash_sting = get_next_hash(global_hash_sting, i)
print(global_hash_sting)
