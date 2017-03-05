#!/usr/bin/python

from sys import *
from http.server import SimpleHTTPRequestHandler
import json
import socketserver
from Crypto.Util.number import *
from Crypto.PublicKey import RSA
from urllib.parse import urlparse

KEY_LENGTH = 512
EXP_LENGTH = 256
PASSWORD = b"6tPFor3d/d9xoSO39GOC/aZY7M++uq74YoNFkERUtGfzVkS02g7ffuj2QLZ0cReEdIPWfrHmExsg"
PORT = 8000
p = getPrime(KEY_LENGTH)
q = getPrime(KEY_LENGTH)

class Handler(SimpleHTTPRequestHandler):
	def do_HEAD(s):
		s.send_response(200, "OK")
		s.send_header("Content-type", "text/html")
		s.end_headers()
	def do_GET(s):
		request = urlparse(s.path)
		path = request[2]
		query = request[4]
		if path == "/":
			sendIndex(s)
		elif path == "/public":
			sendPublicKey(s)
		elif path == "/generate":
			sendNewKeyPair(s)
		elif path == "/flag":
			sendGetKey(s, query)
		else:
			s.send_response(404, "Not Found")
			s.send_header("Content-type", "text/html")
			s.end_headers()

def sendIndex(s):
	s.send_response(200, "OK")
	s.send_header("Content-type", "text/html")
	s.end_headers()
	s.wfile.write(b"<a href='/'>home</a><br>")
	s.wfile.write(b"<a href='/public'>get server's public key/a><br>")
	s.wfile.write(b"<a href='/generate'>generate new RSA key pair</a><br>")
	s.wfile.write(b"<a href='/flag'>get flag (need admin permition)</a><br>")

def sendNewKeyPair(s):
	s.send_response(200, "OK")
	s.send_header("Content-type", "text/plain")
	s.end_headers()
	s.wfile.write(keyToString(generateKeyPair()).encode())

def sendPublicKey(s):
	s.send_response(200, "OK")
	s.send_header("Content-type", "text/plain")
	s.end_headers()
	s.wfile.write(keyToString(serverKey).encode())

def sendGetKey(s, sign):
	if isInt(sign) and serverKey.verify(PASSWORD, [int(sign), 0]):
		s.send_response(200, "OK")
		s.send_header("Content-type", "text/plain")
		s.end_headers()
		s.wfile.write(flag)
	else:
		s.send_response(403, "Forbidden")
		s.send_header("Content-type", "text/plain")
		s.end_headers()
		s.wfile.write(b"403 Forbidden")

def isInt(s):
	try:
		int(s)
		return True
	except ValueError:
		return False

def generateKeyPair():
	p = getPrime(KEY_LENGTH)
	f = (p - 1) * (q - 1);
	e = getRandomInteger(EXP_LENGTH)
	while GCD(e, f) != 1:
		e = getRandomInteger(EXP_LENGTH)
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

def startServer(port):
	httpd = socketserver.TCPServer(("", port), Handler)
	httpd.serve_forever()

flag = open('flag.txt').read().strip().encode()

serverKey = generateKeyPair()
print(keyToString(serverKey))
serverKey = serverKey.publickey()

startServer(PORT)
