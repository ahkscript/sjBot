from bot import bot
import json
from os import listdir
import os
import imp
import urllib.request
import time
import sys
from pprint import pprint

'''
	sjBot is a Python IRC Bot made by Sjc1000 ( Steven J. Core )
			Copyright © 2015, Steven J. Core
	
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


class sjBot(bot):
	def __init__(self, keyfile='keys'):
		self.def_dir = os.path.dirname(os.path.realpath(__file__))
		with open(self.def_dir + '/' + keyfile, 'r') as my_file:
			self.keys = json.loads( my_file.read() )
		self.getsettings()
		pprint('Loading commands and plugins.', prefix=' ', timestamp=1)
		self.commands = self.load_plugins(self.def_dir + '/commands/')
		self.plugins = self.load_plugins(self.def_dir + '/plugins/')
		pprint('Connecting to IRC.', prefix=' ', timestamp=1)
		bot.__init__(self, self.network, self.port)
		self.ident()
		
		try:
			self.main_loop()
		except KeyboardInterrupt:
			pprint('Recieved the command to shutdown.', 'red', prefix=' ', timestamp=1)
			pass
		except:
			pprint('Something went wrong.', 'red', prefix=' ', timestamp=1)
			raise
	
	def getsettings(self):
		with open('sjbot.settings','r') as mfile:
			data = mfile.read()
			settings = json.loads(data)
		required = ['nickname','user','host','realname','network','port','channel_list','default_cmd','botcmd','ignore','ownerlist']
		for test in required:
			if test not in settings:
				print('Setting missing: ' + test)
				sys.exit(0)
				return 0
		for key in settings:
			setattr(self, key, settings[key])
		return 0
	
	def startup(self):
		self.ident()
		self.iterate()
		return 0
	
	def iterate(self, timeout=60):
		while True:
			with open('sjbot.settings') as settings:
				settings = json.loads(settings.read())
			self.botcmd = settings['botcmd']
			self.ownerlist = settings['ownerlist']
			self.ignore = settings['ignore']
			self.default_cmd = settings['default_cmd']
			self.commands = self.load_plugins(self.def_dir + '/commands/')
			self.plugins = self.load_plugins(self.def_dir + '/plugins/')
			time.sleep(timeout)
	
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
			self.send('MONITOR + ' + us)
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
		try:
			response = urllib.request.urlopen(url)
		except:
			return 0 
		return response.read().decode('utf-8')
	
	def onALL(self, *params):
		mtype = params[1]
		
		for pl in self.plugins:
			if hasattr(self.plugins[pl], 'on' + mtype):
				function = getattr(self.plugins[pl], 'on' + mtype)
				function(self, *params)
		return 0

	
	def on730(self, host, nickname, ohost):
		if nickname == self.nickname:
			return 0
		
		user = ohost.split('!')[0][1:]
		uhost = ohost.split('!')[1]
		
		with open(self.def_dir + '/commands/monitor_list', 'r') as mfile:
			monitor_list = json.loads(mfile.read())
		
		for notify in monitor_list:
			for us in monitor_list[notify]:
				if us == user:
					self.notify(notify,'*** ' + us + ' is online ***')
		return 0
	
	def on731(self, host, nickname, ohost):
		if nickname == self.nickname:
			return 0
		
		user = ohost[1:]
		
		with open(self.def_dir + '/commands/monitor_list', 'r') as mfile:
			monitor_list = json.loads(mfile.read())
		
		for notify in monitor_list:
			for us in monitor_list[notify]:
				if us == user:
					self.notify(notify,'*** ' + us + ' is offline ***')
		return 0
	
	def on433(self, host, ast, nickname, *params):
		self.send('NICK ' + nickname + '_')
		self.nickname = nickname + '_'
		pprint('{} already taken. Trying with {}.'.format(nickname, self.nickname), 'yellow', prefix=' ', timestamp=1)
		return 0
	
	def on376(self, host, *params):
		self.send('PRIVMSG Nickserv :Identify sjBot ' + self.keys['sjbot_pass'])
		pprint('Identifying', 'yellow', prefix=' ', timestamp=1)
		return 0
	
	def on396(self, host, chost, *params):
		for channel in self.channel_list:
			self.join(channel)
		pprint('Joining channels: {}'.format(', '.join(self.channel_list)), 'yellow', prefix=' ', timestamp=1)
		self.start_monitor()
		return 0
	
	def onPRIVMSG(self, uhost, channel, *message):
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

			if channel == self.nickname:
				channel = user

			if self.commands[cmd].meta_data['owner'] == 1 and not any(us in uhost for us in self.ownerlist):
				self.privmsg(channel, 'You do not have permission to use that!')
				return 0
			
			response = self.commands[cmd].execute(self, self.commands, user, host, channel, params)
			if response == 0:
				return 0
			for re in response:
				self.privmsg(channel, re.replace('&botcmd', botcmd))
		return 0
	
	def is_command(self, command):
		for cm in self.commands:
			if any( command == c for c in self.commands[cm].meta_data['aliases'] ):
				return cm
		return 0

if __name__ == '__main__':
	sjbot = sjBot()
