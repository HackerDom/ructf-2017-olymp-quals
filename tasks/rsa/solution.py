#!/usr/bin/python

import sys
import requests

import json

from Crypto.Util.number import *
from Crypto.PublicKey import RSA

def get(path, params=None):
	r = requests.get(server + path, params=params)
	return r.text

def getKey(path):
	response = get(path)
	keyString = response.split('\n')[1]
	parts = json.loads(keyString)
	return {'n': parts['n'], 'e': parts['e']}

server = sys.argv[1]
password = sys.argv[2]

public = getKey('/public')
secret = getKey('/generate')

n = public['n']
q = GCD(n, int(secret['n']))
p = n // q
e = public['e']
f = (p - 1) * (q - 1)
d = inverse(e, f)

key = RSA.construct([n, e, d])
sign = key.sign(password.encode(), 0)[0]

print(get('/flag', {'s': sign}))
