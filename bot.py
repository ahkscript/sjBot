import socket
import threading
import time

class ircBot():
	nickname = ''
	user = ''
	host = ''
	realname = ''
	previous_data = b''
	def __init__(self, network, port, parent, attempt_rejoin=1):
		'''__init__
			params:
			- network: The irc network for the bot to join.
			- port: The port for the bot to join.
			- parent: The parent bot class. The bot class will relay data to the parent.
			- attempt_rejoin: Should the bot attempt to rejoin if the connection to IRC is lost.
		'''
		self.network = network
		self.attempt_rejoin = attempt_rejoin
		self.port = port
		self.parent = parent
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect((network,port))
	
	def send(self, data, prefix='', suffix='\r\n'):
		'''send
		Sends data to IRC.
		params:
		- data: The data to send to IRC
		- prefix: Stuff to add to the start of data.
		- suffix: Stuff to add to the end. Defaults to a newline. 
		'''
		self.socket.send(bytes(prefix + data + suffix, 'utf-8'))
		return 0
	
	def privmsg(self, channel, data):
		'''privmsg
		Sends a PRIVMSG to a channel.
			params:
			- channel: The channel to send the data to.
			- data: The data to send to IRC.
		'''
		self.send('PRIVMSG ' + channel + ' :' + data)
		return 0
	
	def notify(self, user, data):
		'''notify
		Sends a notify to a channel.
			params:
			- user: The channel / user to send the data to.
			- data: The data to send.
		'''
		self.send('NOTICE ' + user + ' :' + data)
		return 0
	
	def join(self, channellist):
		'''join
		Joins a list of channels.
			params:
			- channellist: A list of channels to join. Specify a string to only join 1.
		'''
		if isinstance(channellist, str):
			channellist = [channellist]
		for channel in channellist:
			self.send('JOIN ' + channel)
		return 0
	
	def ident(self, nickname, user, host, realname):
		'''ident
		Identifies the bot.
			params:
			- nickname: The nickname of the bot.
			- user: The bots user.
			- host: The bots host.
			- realname: The real name of the bot.
		'''
		self.send('NICK ' + nickname)
		self.send('USER ' + ' '.join([nickname, user, host]) + ' :' + realname)
		self.nickname = nickname
		self.user = user
		self.host = host
		self.realname = realname
		return 0
	
	def iterate(self, timeout=30):
		'''iterate
		This is method is called from the parent to start an iterate thread. The iterate thread calls the parents onITERATE method every x seconds. This is used for things such as auto updates and getting forum feeds. etc. etc.
			params:
			- timeout: The ammount of seconds to sleep between iterations.
		'''
		while True:
			if hasattr(self.parent, 'onITERATE'):
				function = getattr(self.parent, 'onITERATE')
				data_thread = threading.Thread(target=function)
				data_thread.daemon = True
				data_thread.start()
			
			time.sleep(timeout)
		return -1
	
	def message_parent(self, data):
		'''message_parent
		Calls the parent's sys_message method. Which can then do anything with the message.
			params:
			- data: The data to send to the parent.
		'''
		if hasattr(self.parent, 'sys_message'):
			function = getattr(self.parent, 'sys_message')
			function(data)
		return 0
	
	def data_loop(self):
		'''data_loop
		The data loop which handles incoming data from IRC. It will then pass it to handle_data when a complete ammount of data has been retrieved.
		'''
		while True:
			recv_data = self.socket.recv(1024)
			if len(recv_data) == 0:
				self.shutdown()
			
			if recv_data.endswith(b'\r\n'):
				self.handle_data(self.previous_data + recv_data)
				self.previous_data = b''
			else:
				self.previous_data = self.previous_data + recv_data
		return -1
	
	def shutdown(self):
		'''shutdown
		Called when there is no data recieved from IRC anymore.
		If attempt_rejoin has been set to 1 it will try 10 times to reconnect.
		'''
		self.message_parent('IRC connection lost.')
		if self.attempt_rejoin == 1:
			self.message_parent('Retrying connection.')
			for i in range(1,10):
				self.message_parent('Attempt {}'.format(str(i)))
				self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				
				try:
					self.socket.connect((self.network, self.port))
				except TimeoutError:
					self.message_parent('Attempt failed.')
					time.sleep(10)
				else:
					self.message_parent('Attempt succesful.')
					self.ident(self.nickname, self.user, self.host, self.realname)
					break
		return 0
	
	def handle_data(self, data):
		'''handle_data
		Handles the data from IRC. Calls onTYPE if the parent class has the right method. Example onPRIVMSG
			params:
			- data: The data recieved from IRC
		'''
		try:
			data = data.decode('utf-8')
		except UnicodeDecodeError:
			return 0
		for line in data.split('\r\n'):
			if line == '':
				continue
			split = line.split(' ')
			
			if split[0] == 'PING':
				self.send('PONG ' + split[1][1:])
			
			if hasattr(self.parent, 'on' + split[1]):
				params = [split[0]] + split[2:]
				function = getattr(self.parent, 'on' + split[1])
				data_thread = threading.Thread(target=function, args=params)
				data_thread.daemon = True
				data_thread.start()
			
			if hasattr(self.parent, 'onALL'):
				function = getattr(self.parent, 'onALL')
				data_thread = threading.Thread(target=function, args=[split])
				data_thread.daemon = True
				data_thread.start()
		return 0


if __name__ == '__main__':
	print('This file should not be ran at all. Its a class to be imported.')
	inp = input('Do you wish to see the help for this class? ')
	
	if inp.lower() == 'yes':
		help(ircBot)
