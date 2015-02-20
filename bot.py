import irc
import threads
import os
import sys
import imp
import time
from os import listdir
import json
import urllib.request

class _bot():
	def __init__(self, network, port, parent_dir, prefix='on'):
		self.parent_name = parent_dir.split('/')[-1]
		self.parent_dir = parent_dir
		self.parent = imp.load_source( self.parent_name, self.parent_dir )
		self.irc = irc.client(network, port)
		self.running = 1
		self.thread = threads.thread(10)
		self.prefix = prefix
		self.default_dir = os.path.dirname(os.path.realpath(__file__))
		
		with open(self.default_dir + '/keys') as my_file:
			self.keys = json.loads( my_file.read() )
		
		self.call_parent('START', '')
		self.thread.add_task('iterate', '', self)
	
	def iterate(self):
		while True:
			time.sleep(30)
			self.call_parent('ITERATE', 'iterate')
			self.parent = imp.load_source( self.parent_name, self.parent_dir )
			self.thread.add_task('call_parent', ['ALL', ('ITERATE', 'iterate')], self)
		return -1
	
	def call_parent(self, module, params):
		if not hasattr(self.parent, self.prefix + module):
			return -1
		return getattr(self.parent, self.prefix + module)(self, *params)
	
	def ident(self, username):
		self.irc.ident(username)
	
	def shorten_url(self, url):
		return self.download_url('https://api-ssl.bitly.com/v3/shorten?access_token=' + self.keys['bitly'] + '&format=txt&Longurl=' + url)
		
	def download_url(self, url):
		try:
			response = urllib.request.urlopen(url)
			response_data = response.read().decode('utf-8')
		except UnicodeDecodeError:
			raise UnicodeDecodeError('response.read().decode()')
		return response_data
	
	def main_loop(self):
		self.previous_data = b''
		while True:
			recieved = self.irc.recv()
			if len(recieved) == 0:
				self.call_parent('onQUIT', 'No Data')
				self.irc.stop()
				break
			if recieved.endswith(b'\r\n'):
				self.handle_data(self.previous_data + recieved)
				self.previous_data = b''
			else:
				self.previous_data = self.previous_data + recieved
		return -1
	
	def handle_data(self, data):
		try:
			data = data.decode('utf-8')
		except UnicodeDecodeError:
			return -1
		
		lines = data.split('\r\n')
		for line in lines:
			if line == '':
				continue
			print('> ' + line) 
			split = line.split(' ')
			if split[0] == 'PING':
				self.irc.pong(split[1][1:])
			
			if len(split) > 2:
				params = [ split[0][1:] ] + split[2:]
				self.thread.add_task('call_parent', [split[1], params], self)
				self.thread.add_task('call_parent', ['ALL', (split[1], params)], self)
		return 0
	
	def load_plugins(self, folder, prefix):
		files = listdir(folder)
		plugins = {}
		for f in files:
			if not f.endswith('.py'):
				continue
			module_name = f[:f.index('.')]
			setattr(sys.modules['__main__'], prefix + module_name, imp.load_source(module_name, folder + f))
			plugins[module_name] = imp.load_source(module_name, folder + f)
		return plugins
		
