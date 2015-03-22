import bot
import json
from os import listdir
import os
import imp
import urllib.request
import time
import sys
from pprint import pprint

class sjBot(bot.ircBot):
	botcmd = {'default': '`','#donationcoder': '.'}
	default_cmd = {'default': 'ahk', '#donationcoder': 'google'}
	ignore = ['.','n','r','`']
	ownerlist = ['Sjc1000@gateway/shell/elitebnc']
	botname = 'sjBot'
	channel_list = ['#Sjc_Bot','#ahkscript','#ahk','#donationcoder']
	def __init__(self, network, port, keyfile='keys'):
		self.def_dir = os.path.dirname(os.path.realpath(__file__))
		pprint('{} started. Thanks for using my software! :D'.format(self.botname), prefix=' ', timestamp=1)
		with open(self.def_dir + '/' + keyfile, 'r') as my_file:
			self.keys = json.loads( my_file.read() )
		pprint('Loading commands and plugins.', prefix=' ', timestamp=1)
		self.commands = self.load_plugins(self.def_dir + '/commands/')
		self.plugins = self.load_plugins(self.def_dir + '/plugins/')
		pprint('Connecting to IRC.', prefix=' ', timestamp=1)
		self.irc = bot.ircBot(network, port, self)
		self.irc.ident(self.botname, self.botname, self.botname, 'Uptone Software')
		
		try:
			self.irc.data_loop()
		except KeyboardInterrupt:
			pprint('Recieved the command to shutdown.', 'red', prefix=' ', timestamp=1)
			self.shutdown()
		except:
			pprint('Something went wrong.', 'red', prefix=' ', timestamp=1)
			raise
	
	def shutdown(self):
		self.irc.send('QUIT :Ive been told to quit. Bye :D')
		self.irc.socket.shutdown(1)
		self.irc.socket.close()
		return 0
	
	def start_monitor(self):
		pprint('Starting user monitor.', 'yellow', prefix=' ', timestamp=1)
		with open(self.def_dir + '/commands/monitor_list', 'r') as mfile:
			monitor_list = json.loads(mfile.read())
		users = []
		
		for musers in monitor_list:
			for us in monitor_list[musers]:
				if us not in users:
					users.append(us)
		for us in users:
			self.irc.send('MONITOR + ' + us)
		return 0
	
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
		response 	= urllib.request.urlopen(url) 
		return response.read().decode('utf-8')
	
	def onALL(self, params):
		self.plugins = self.load_plugins(self.def_dir + '/plugins/')
		mtype = params[1]
		
		for pl in self.plugins:
			if hasattr(self.plugins[pl], 'on' + mtype):
				function = getattr(self.plugins[pl], 'on' + mtype)
				function(self, *params)
		return 0

	
	def on730(self, host, nickname, ohost):
		if nickname == self.botname:
			return 0
		
		user = ohost.split('!')[0][1:]
		uhost = ohost.split('!')[1]
		
		with open(self.def_dir + '/commands/monitor_list', 'r') as mfile:
			monitor_list = json.loads(mfile.read())
		
		for notify in monitor_list:
			for us in monitor_list[notify]:
				if us == user:
					self.irc.notify(notify,'*** ' + us + ' is online ***')
		return 0
	
	def on731(self, host, nickname, ohost):
		if nickname == self.botname:
			return 0
		
		user = ohost[1:]
		
		with open(self.def_dir + '/commands/monitor_list', 'r') as mfile:
			monitor_list = json.loads(mfile.read())
		
		for notify in monitor_list:
			for us in monitor_list[notify]:
				if us == user:
					self.irc.notify(notify,'*** ' + us + ' is offline ***')
		return 0
	
	def on433(self, host, ast, nickname, *params):
		self.irc.send('NICK ' + nickname + '_')
		self.botname = nickname + '_'
		pprint('{} already taken. Trying with {}.'.format(nickname, self.botname), 'yellow', prefix=' ', timestamp=1)
		return 0
	
	def on376(self, host, *params):
		self.irc.send('PRIVMSG Nickserv :Identify sjBot ' + self.keys['sjbot_pass'])
		pprint('Identifying', 'yellow', prefix=' ', timestamp=1)
		return 0
	
	def on396(self, host, chost, *params):
		self.irc.join(self.channel_list)
		pprint('Joining channels: {}'.format(', '.join(self.channel_list)), 'yellow', prefix=' ', timestamp=1)
		self.start_monitor()
		return 0
	
	def onPRIVMSG(self, uhost, channel, *message):
		self.commands = self.load_plugins(self.def_dir + '/commands/')
		user, host = uhost.split('!')
		user = user[1:]
		message = [x for x in message]
		message = [message[0][1:]] + message[1:]
		
		if channel in self.botcmd:
			botcmd = self.botcmd[channel]
		else:
			botcmd = self.botcmd['default']
		
		if message[0].startswith(botcmd):
			command = message[0][len(botcmd):]
			
			if any(command.startswith(c) for c in self.ignore):
				return 0

			params = message[1:]
			
			cmd = self.is_command(command.lower())
			
			if cmd == 0:
				if channel in self.default_cmd:
					cmd = self.default_cmd[channel]
				else:
					cmd = self.default_cmd['default']
				params = [message[0][len(botcmd):]] + message[1:]

			if channel == self.botname:
				channel = user

			if self.commands[cmd].meta_data['owner'] == 1 and not any(us in uhost for us in self.ownerlist):
				self.irc.privmsg(channel, 'You do not have permission to use that!')
				return 0
			
			response = self.commands[cmd].execute(self, self.commands, self.irc, user, host, channel, params)
			if response == 0:
				return 0
			for re in response:
				self.irc.privmsg(channel, re.replace('&botcmd', botcmd))
		return 0
	
	def is_command(self, command):
		for cm in self.commands:
			if any( command == c for c in self.commands[cm].meta_data['aliases'] ):
				return cm
		return 0

if __name__ == '__main__':
	sjbot = sjBot('irc.freenode.net', 6667)
