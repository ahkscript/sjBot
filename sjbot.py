import bot
import json
from os import listdir
import os
import imp
import urllib.request

class sjBot(bot.ircBot):
	botcmd = '.'
	botname = 'sjBot'
	def __init__(self, network, port, keyfile='keys'):
		self.def_dir = os.path.dirname(os.path.realpath(__file__))
		print('[ Loading keyfile')
		with open(self.def_dir + '/' + keyfile, 'r') as my_file:
			self.keys = json.loads( my_file.read() )
		print('[ Loading commands and plugins.')
		self.commands = self.load_plugins(self.def_dir + '/commands/')
		self.plugins = self.load_plugins(self.def_dir + '/plugins/')
		print('[ Connecting to irc.\n\tNetwork: ' + network + '\n\tPort: ' + str(port))
		self.irc = bot.ircBot(network, port, self)
		print('[ Identifying with username ' + self.botname + '.')
		self.irc.ident(self.botname, self.botname, self.botname, 'Uptone Software')
		print('[ Creating main data loop.')
		self.irc.data_loop()
	
	def load_plugins(self, plugin_folder):
		plugins = {}
		files = listdir(plugin_folder)
		for f in files:
			if not f.endswith('.py'):
				continue
			name = f[:f.index('.')]
			plugins[name] = imp.load_source('pl_' + name, plugin_folder  + f)
		return plugins
	
	def shorten_url(self, url):
		response = self.download_url('https://api-ssl.bitly.com/v3/shorten?access_token=' + self.keys['bitly'] + '&format=txt&Longurl=' + url)
		if response == 0:
			return url
		return response
	
	def download_url(self, url):
		try:
			response 	= urllib.request.urlopen(url) 
		except UnicodeEncodeError:
			return 0
		except:
			return 0
		return response.read().decode('utf-8')
	
	def onALL(self, params):
		mtype = params[1]
		
		for pl in self.plugins:
			if hasattr(self.plugins[pl], 'on' + mtype):
				function = getattr(self.plugins[pl], 'on' + mtype)
				function(self, params)
		return 0
	
	def onITERATE(self):
		self.commands = self.load_plugins(self.def_dir + '/commands/')
		self.plugins = self.load_plugins(self.def_dir + '/plugins/')
		return 0
	
	def on433(self, host, ast, nickname, *params):
		self.irc.send('NICK ' + nickname + '_')
		self.botname = nickname + '_'
		return 0
	
	def on376(self, host, *params):
		self.irc.send('PRIVMSG Nickserv :Identify sjBot ' + self.keys['sjbot_pass'], star=self.keys['sjbot_pass'])
	
	def on396(self, host, chost, *params):
		self.irc.join(['#ahk', '#ahkscript', '#Sjc_Bot'])
		return 0
	
	def onITERATE(self):
		self.commands = self.load_plugins(self.def_dir + '/commands/')
		self.plugins = self.load_plugins(self.def_dir + '/plugins/')
		return 0
	
	def onPRIVMSG(self, uhost, channel, *message):
		user, host = uhost.split('!')
		user = user[1:]
		message = [x for x in message]
		message = [message[0][1:]] + message[1:]
		
		if channel == self.botname:
			channel = user
		
		if message[0].startswith(self.botcmd):
		
			command = message[0][len(self.botcmd):]
			params = message[1:]
			
			cmd = self.is_command(command)
			
			if cmd == 0:
				command = 'ahk'
				params = [message[0][len(self.botcmd):]] + message[1:]
			response = self.commands[cmd].execute(self, self.commands, self.irc, user, host, channel, params)
			for re in response:
				self.irc.privmsg(channel, re)
		return 0
	
	def is_command(self, command):
		for cm in self.commands:
			if any( command == c for c in self.commands[cm].meta_data['aliases'] ):
				return cm
		return 0

if __name__ == '__main__':
	sjbot = sjBot('irc.freenode.net', 6667)
