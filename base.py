#!/usr/bin/env python3
"""
A simple IRC base for python3.
This class makes using IRC easy.
"""


import socket
import time
import sys
import threads
from cprint import cprint


class base():

	previous = b''
	password = None
	queue = []
	connected = False

	def __init__(self, network, port, nickname, user, host, realname,
				 rejoin=True):
		"""__init__
		Starts the bot base.
		
		params:
			network:	The network for the irc bot to join.
			port:		The port for the bot to join.
			rejoin:		True if you want the bot to attempt to rejoin
						when he disconnects.
		"""
		self.nickname = nickname
		self.host = host
		self.user = user
		self.realname = realname
		self.network = network
		self.port = port
		self.rejoin = rejoin
		self.onSTARTUP()

	def connect(self, attempts=10, delay=10):
		"""connect
		Attempts to connect to IRC.

		params:
			attempts:	The amount of times to try to connect.
						10 seconds ( by default ) in between each try.
			delay:		The delay in seconds between each try. 10 by default.
		"""
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.display('Attempting to connect to IRC.')
		self.connceted = False
		for attempt in range(0, attempts):
			try:
				self.display('Attempt ' + str(attempt))
				self.socket.connect((self.network, self.port))
			except TimeoutError:
				self.display('Connection attempt ' + str(attempt + 1) + 
							 ' failed.')
				time.sleep(delay)
				continue
			else:
				self.connected = True
				self.display('[.green]Connected.')
				self.identify(self.nickname, self.user, self.host,
							  self.realname)
				return True
		return False

	def onSTARTUP(self):
		"""onSTARTUP
		Called when the bot's __init__ finished.
		This also happens before the connecting.
		If you overright this, you will need to call .connect at some later
		time.
		"""
		connected = self.connect()
		if connected is False:
			self.display('Could not connect. Shutting down.')
			self.shutdown()
		return None

	def identify(self, nickname, user, host, realname, password=None):
		"""identify
		Identifies the bot.

		params:
			nickname:	The nickname for the bot to use.
			user:		The user for the bot to use.
			host:		The host of the bot.
			realname:	The real name of the bot.
			password:	The password for the server. Please note:
						This IS NOT the password for server's bot such as 
						freenode's Nickserv. You will need to send the 
						password at some other time.
		"""
		self.nickname = nickname
		self.user = user
		self.host = host
		self.realname = realname
		if password is not None:
			self.password = password
			self.send('PASS ' + password)
		self.send('NICK ' + nickname)
		self.send('USER ' + nickname + ' ' + user + ' ' + host + ' :' + 
				  realname)
		return None

	def send(self, data):
		"""send
		A wrapper for the normal socket send. This converts the data param
		into bytes and auto appends a newline.

		params:
			data:	The data to send to IRC.
		"""
		if isinstance(data, list):
			for d in data:
				self.send(d)
			return None
		self.display('< ' + data, 'green')
		sent = self.socket.send(bytes(data + '\r\n', 'utf-8'))
		if sent == 0:
			self.try_rejoin()
		return None

	def main_loop(self):
		"""main_loop
		The main data recieving loop for the IRC bot. This section will
		get the data, if the data isn't full it will wait until it gets all
		the data. Then it will send it to handle_data.
		"""
		while True:
			try:
				recv = self.socket.recv(1024)

				if recv == '':
					for i in range(0, 10):
						recv = self.socket.recv(1024)
						if recv != '':
							break
						if i == 9:
							if self.try_rejoin() is False:
								return None

			except OSError:
				if self.rejoin:
					connected = self.connect()
					if connected is False:
						self.shutdown()
						self.display('Could not reconnect. Shutting down.')
					continue

			if recv.endswith(b'\r\n'):
				self.handle_data(self.previous + recv)
				self.previous = b''
			else:
				self.previous += recv
		return None

	def try_rejoin(self):
		"""try_rejoin
		Attempts to rejoin to IRC. Only if the self.rejoin is set
		to True.
		"""
		if self.rejoin is True:
			connected = self.connect()
			if connected is False:
				return False
			return True
		return False

	def handle_data(self, data):
		"""handle_data
		This will handle data incoming from the main_loop.
		This is where all the action happens. It splits it up and turns things
		into onMESSAGE setups. messages will be things like JOIN, PART and
		other IRC things.

		params:
			data:	The data to handle.
		"""
		try:
			data = data.decode('utf-8')
		except UnicodeDecodeError:
			return None

		for line in data.split('\r\n'):
			if line == '':
				continue
			self.display('> ' + line, 'yellow')
			split = line.split(' ')
			if len(split) < 2:
				continue
			
			queue = self.queue
			for index, event in enumerate(queue):
				if event['event'] == split[1]:
					self.queue[index]['function'](*self.queue[index]['params'])
				self.queue.pop(index)

			if hasattr(self, 'onALL'):
				self.onALL(*split)

			if hasattr(self, 'on' + split[0]):
				getattr(self, 'on' + split[0])(*split[1:])
			if hasattr(self, 'on' + split[1]):
				getattr(self, 'on' + split[1])(*[split[0]] + split[2:])
		return None

	def on433(self, *junk):
		"""on433
		Happens when the current nickname is taken.
		This function appends a _ then tries again.
		"""
		self.nickname = self.nickname + '_'
		self.send('NICK ' + self.nickname)
		return None

	def onERROR(self, *params):
		"""onERROR
		Called when an error is found in the IRC data.
		"""
		if ' '.join(params[:2]) == ':Closing Link:':
			if self.try_rejoin() is True:
				return None
			self.shutdown()
		return None

	def onPING(self, *params):
		"""onPING
		Called when the bot finds a ping message.
		It will then send a pong back to the server.
		"""
		self.send('PONG ' + params[0])
		return None

	def shutdown(self):
		"""shutdown
		The shutdown function. This will close connection to IRC.
		It will also display the message 'Shutting down'.
		"""
		if self.connected == False:
			self.display('Could not connect to IRC. Shutting down.')
			return None
		self.display('Shutting down.')
		self.send('QUIT :Shutting down.')
		self.socket.close()
		return None

	def display(self, data, color='purple'):
		"""display
		Displays some text in the IRC. This is basically a wrapper for
		the print function, although, you can add your own to your bot class
		this means you can overright my bots printing to suit you. 
		For example, you can make your own display method where it puts a
		timestamp inront of all messages.

		params:
			data:	The data that gets displayed.
		"""
		cprint('[.' +  color + ']' + data)
		return None

	def privmsg(self, channel, data):
		"""privmsg
		Sends a privmsg to IRC.

		params:
			channel:	The channel to send it to. If this is a username it
						will be a query ( you may know this as PM or by 
						another name ).
		"""
		self.send('PRIVMSG ' + channel + ' :' + data)
		return None

	def action(self, channel, action):
		"""action
		A privmsg wrapper that makes the bot do an action. In irc
		it will look something like   * bot just entered the room

		params:
			channel:	The channel to send the action to.
			action:		The string to use as the action.
		"""
		self.privmsg(channel, '\x01ACTION ' + action + '\x01')
		return None

	def join(self, channel):
		"""join
		Joins a channel.

		params:
			channel:	The channel to join.
		"""
		if isinstance(channel, list):
			for chan in channel:
				self.send('JOIN ' + chan)
			return None
		self.send('JOIN ' + channel)
		return None

	def leave(self, channel):
		"""leave
		Leaves a channel.

		params:
			channel:	The channel to leave.
		"""
		if isinstance(channel, list):
			for chan in channel:
				self.send('PART ' + chan)
			return None
		self.send('PART ' + channel)
		return None

	def nick(self, nickname):
		"""nick
		Changes the nickname of the bot.

		params:
		 nickname:	The new nickname of the bot.
		"""
		self.nickname = nickname
		self.send('NICK ' + nickname)
		return None

	def notify(self, user, data):
		"""notify
		Sends a NOTICE to the user.

		params:
			user:	The user to send the data to.
			data:	The data to send to the user.
		"""
		self.send('NOTICE ' + user + ' :' + data)
		return None


if __name__ == '__main__':
	help(base)