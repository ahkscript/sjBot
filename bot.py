import socket
import threading
import time

class ircBot():
	def __init__(self, network, port, parent):
		self.parent = parent
		self.previous_data = b''
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.connect((network,port))
	
	def send(self, data, prefix='', suffix='\r\n', star=''):
		self.socket.send(bytes(prefix + data + suffix, 'utf-8'))
		print('< ' + prefix + data.replace(star, '*' * len(star)) + suffix.replace('\r\n', ''))
		return 0
	
	def privmsg(self, channel, data):
		self.send('PRIVMSG ' + channel + ' :' + data)
		return 0
	
	def notify(self, user, data):
		self.send('NOTICE ' + user + ' :' + data)
		return 0 
	
	def join(self, channellist):
		if isinstance(channellist, str):
			channellist = [channellist]
		for channel in channellist:
			self.send('JOIN ' + channel)
		return 0
	
	def ident(self, nickname, user, host, realname):
		self.send('NICK ' + nickname)
		self.send('USER ' + ' '.join([nickname, user, host]) + ' :' + realname)
		return 0
	
	def iterate(self, timeout=30):
		while True:
			if hasattr(self.parent, 'onITERATE'):
				function = getattr(self.parent, 'onITERATE')
				data_thread = threading.Thread(target=function)
				data_thread.daemon = True
				data_thread.start()
			
			time.sleep(timeout)
		return -1
	
	def data_loop(self):
		while True:
			recv_data = self.socket.recv(1024)
			if len(recv_data) == 0:
				self.shutdown()
				break
			
			if recv_data.endswith(b'\r\n'):
				self.handle_data(self.previous_data + recv_data)
				self.previous_data = b''
			else:
				self.previous_data = self.previous_data + recv_data
		return -1
	
	def shutdown(self):
		return 0
	
	def handle_data(self, data):
		try:
			data = data.decode('utf-8')
		except UnicodeDecodeError:
			return 0
		for line in data.split('\r\n'):
			if line == '':
				continue
			print('> ' + line)
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
