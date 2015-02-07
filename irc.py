import socket
import time

class client():
	def __init__(self, server, port):
		self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.irc.connect((server, port))

	def send(self, data):
		self.irc.send(bytes(data, 'utf-8') + b'\r\n')
		print('< ' + data)
		return 0

	def privmsg(self, channel, message):
		self.send('PRIVMSG ' + channel + ' :' + message)
		return 0
	
	def ident(self, nickname):
		self.nickname = nickname
		self.send('NICK ' + nickname)
		self.send('USER ' + nickname + ' ' + nickname + ' ' + nickname + ' :Uptone_Software')
		return 0

	def nick(self, nickname):
		self.nickname = nickname
		self.send('NICK ' + nickname)
		return 0

	def join(self, channels):
		if channels == ['']:
			return -1
		for ch in channels:
			self.send('JOIN ' + ch)
		return 0

	def leave(self, channels):
		if channels == ['']:
			return -1
		for ch in channels:
			self.send('PART ' + ch)
		return 0

	def pong(self, server):
		self.send('PONG ' + server)
		return 0

	def recv(self, size=1024):
		return self.irc.recv(size)

	def monitor(self, users):
		for user in users:
			self.send('MONITOR + ' + user)
		return 0

	def stop_monitor(self, users):
		for user in users:
			self.send('MONITOR - ' + user)
		return 0

	def notice(self, user, data):
		self.send('NOTICE ' + user + ' :' + data)
		return 0

	def stop(self):
		self.irc.shutdown(1)
		self.irc.close()
		return 0
