#!/usr/bin/env python3


import socket
import threading
import sys


'''
	sjBot is a Python IRC Bot made by Sjc1000 ( Steven J. Core )
			Copyright © 2015, Steven J. Core
	
	This file is a part of sjBot.
	
	sjBot is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the 
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


class bot():

	previous = b''
	password = None

	def __init__(self, network, port, rejoin=1):
		"""__init__
		Creates an IRC connection.
		params:
			network:	The network to join.
			port:		The port to join on.
			rejoin:		Should the bot rejoin if he disconnects.
		"""
		self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.network = network
		self.port = port
		self.rejoin = rejoin
		self.make_connection()
		self.startup()
	
	def make_connection(self):
		"""make_connection
		Attempts to make a connection to IRC.
		"""
		for i in range(0,10):
			try:
				self.irc.connect((self.network, self.port))
			except TimeoutError:
				continue
			else:
				return 1
		return 0
	
	def startup(self):
		"""startup
		Initiates the bot
		"""
		self.nickname,self.user,self.host,self.realname = (
				'sjBot','sjBot','sjBot','Uptone Software')
		self.ident()
		self.main_loop()
		return 0
	
	def send(self, data):
		"""send
		Sends some data to IRC.
		params:
			data:	The data to send.
		"""
		self.irc.send(bytes(data+'\r\n','utf-8'))
		return 0
	
	def privmsg(self, channel, data):
		"""privmsg
		Sends a privmsg to a channel.
		params:
			channel:	The channel to send to.
			data:		The data to send
		"""
		self.send('PRIVMSG ' + channel + ' :' + data)
		return 0
	
	def notice(self, user, data):
		"""notice
		Sends a notice to a user.
		params:
			user:	The user to send the data to.
			data:	The data to send.
		"""
		self.send('NOTICE ' + user + ' :' + data)
		return 0
	
	def ident(self):
		"""ident
		Identifies the bot.
		"""
		if self.password is not None:
			self.send('PASS ' + password)
		self.send('NICK ' + self.nickname)
		self.send('USER ' + ' '.join((self.nickname, self.user, self.host,
				  self.realname)))
		return 0
	
	def main_loop(self):
		"""main_loop
		The main receiving loop
		"""
		while True:
			recv = self.irc.recv(1024)
			if len(recv) == 0:
				self.shutdown()
			if recv.endswith(b'\r\n'):
				self.handle_data(self.previous + recv)
				self.previous = b''
			else:
				self.previous = self.previous + recv
		return 0
	
	def onPING(self, host):
		"""onPING
		PINGS the server.
		"""
		self.send('PONG ' + host)
		return 0
	
	def on376(self, *params):
		if self.channels != []:
			for channel in self.channels:
				self.join(channel)
		return 0
	
	def on433(self, host, p, nickname, *params):
		self.nickname = nickname + '_'
		self.send('NICK ' + self.nickname)
		return 0
	
	def join(self, channel):
		self.send('JOIN ' + channel)
		return 0
	
	def leave(self, channel):
		self.send('PART ' + channel)
		return 0
	
	def handle_data(self, data):
		try:
			data = data.decode('utf-8')
		except UnicodeDecodeError:
			return 0

		for line in data.split('\r\n'):
			split = line.split(' ')
			print( line )
			if split[0] == 'PING':
				self.onPING(split[1])
				continue
			
			if len(split) > 2:
				if hasattr(self, 'on' + split[1]):
					params = [split[0]] + split[2:]
					function = getattr(self, 'on' + split[1])
					call_thread = threading.Thread(target=function, args=params)
					call_thread.daemon = True
					call_thread.start()
				
				if hasattr(self, 'onALL'):
					params = split
					function = getattr(self, 'onALL')
					call_thread = threading.Thread(target=function, args=params)
					call_thread.daemon = True
					call_thread.start()
		return 0
	
	def onALL(self, *params):
		pass
	
	def shutdown(self):
		connection = 0
		if self.rejoin == 1:
			connection = self.make_connection()
		
		if connection == 0:
			self.irc.shutdown(0)
			self.irc.close()
			sys.exit(0)
		return 0


if __name__ == '__main__':
	print('This file is not meant to be ran. It is a file to be imported!')
	print('bot.py is an IRC bot class made by Sjc1000 for the use in sjBot '
		  'also made by Sjc1000')