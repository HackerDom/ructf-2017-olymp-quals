#!/usr/bin/python

import asyncio
from aiohttp import web

import json

from Crypto.Util.number import *
from Crypto.PublicKey import RSA
import os
import urllib.parse

KEY_LENGTH = 512
PASSWORD = b"6tPFor3d/d9xoSO39GOC/aZY7M++uq74YoNFkERUtGfzVkS02g7ffuj2QLZ0cReEdIPWfrHmExsg"
PORT = int(os.environ.get('PORT', '8000'))

async def sendIndex(request):
	return web.Response(content_type='text/html', text='''
		<a href='/'>home</a><br>
		<a href='/public'>get server's public key</a><br>
		<a href='/generate'>generate new RSA key pair</a><br>
		<a href='/flag'>get flag (need admin permition)</a><br>
	''')

async def sendNewKeyPair(request):
	return web.Response(text=keyToString(generateKeyPair()))


async def sendPublicKey(request):
	return web.Response(text=serverKeyString)

async def sendFlag(request):
	params = urllib.parse.parse_qs(request.query_string)
	try:
		s = int(params['s'][0])
		if serverKey.verify(PASSWORD, [s, 0]):
			return web.Response(text=flag)
	except:
		pass
	return web.Response(status='403', text='403 Forbidden')

def generateKeyPair():
	p = getPrime(KEY_LENGTH)
	return generateKeyPairByPrimes(p, q)

def generateKeyPairByPrimes(p, q):
	f = (p - 1) * (q - 1);
	e = 3
	while GCD(e, f) != 1:
		e += 2
	d = inverse(e, f)
	return RSA.construct([p * q, e, d])

def keyToString(key):
	res = '### ';
	if key.has_private():
		res += 'PRIVATE'
	else:
		res += 'PUBLIC'
	res += ' RSA KEY ###\n'
	dic = {'n' : key.n, 'e' : key.e}
	if key.has_private():
		dic['d'] = key.d
	return res + json.dumps(dic)

def makeApp():
	loop = asyncio.get_event_loop()
	app = web.Application(loop=loop)
	app.router.add_get('/', sendIndex)
	app.router.add_get('/generate', sendNewKeyPair)
	app.router.add_get('/public', sendPublicKey)
	app.router.add_get('/flag', sendFlag)
	return app

with open('flag.txt') as flagFile:
	flag = flagFile.read().strip()

with open('key', 'r') as key:
	p = int(key.readline().strip())
	q = int(key.readline().strip())

serverKey = generateKeyPairByPrimes(p, q)
print(keyToString(serverKey))
serverKey = serverKey.publickey()
serverKeyString = keyToString(serverKey)

app = makeApp()

if __name__ == '__main__':
	web.run_app(app, port=PORT)
