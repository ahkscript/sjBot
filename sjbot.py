import bot
import json
from os import listdir
import os
import imp
import urllib.request
import time


tc = {'header':'\033[95m','blue':'\033[94m','green':'\033[92m','warning':'\033[93m',
	'fail':'\033[91m','end':'\033[0m','bold':'\033[1m','underline':'\033[4m'}

class sjBot(bot.ircBot):
	botcmd = '`'
	botname = 'sjBot'
	channel_list = ['#Sjc_Bot']
	def __init__(self, network, port, keyfile='keys'):
		self.def_dir = os.path.dirname(os.path.realpath(__file__))
		self.prout('Starting IRC bot.','green')
		with open(self.def_dir + '/' + keyfile, 'r') as my_file:
			self.keys = json.loads( my_file.read() )
		self.prout(['Loading plugins.','Loading commands.'])
		self.commands = self.load_plugins(self.def_dir + '/commands/')
		self.plugins = self.load_plugins(self.def_dir + '/plugins/')
		self.prout(['Connecting to irc.','Network: ' + network,'Port: ' + str(port)])
		self.irc = bot.ircBot(network, port, self)
		self.prout('Identifying with username ' + self.botname + '.')
		self.irc.ident(self.botname, self.botname, self.botname, 'Uptone Software')
		self.prout('Creating main data loop.')
		self.irc.data_loop()
	
	def prout(self, data, tcolor=''):
		t = time.localtime(time.time())
		if tcolor == '':
			color = ''
		else:
			color = tc[tcolor]
		if isinstance(data, str):
			print('{0}[{1:0>2}:{2:0>2}:{3:0>2}]{4}{5} {6}{4}'.format(tc['header'],t[3],t[4],t[5],tc['end'],color,data))
		else:
			for line in data:
				print('{0}[{1:0>2}:{2:0>2}:{3:0>2}]{4}{5} {6}{4}'.format(tc['header'],t[3],t[4],t[5],tc['end'],color,line))
		return 0
	
	def start_monitor(self):
		self.prout('Starting user monitor.')
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
				function(self, params)
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
		self.prout('Nickname: {} already in use. Trying with {}'.format(nickname, nickname + '_'))
		return 0
	
	def on376(self, host, *params):
		self.irc.send('PRIVMSG Nickserv :Identify sjBot ' + self.keys['sjbot_pass'])
		return 0
	
	def on396(self, host, chost, *params):
		self.irc.join(self.channel_list)
		self.prout('Joining channels: {}'.format(', '.join(self.channel_list)))
		self.start_monitor()
		return 0
	
	def onPRIVMSG(self, uhost, channel, *message):
		self.commands = self.load_plugins(self.def_dir + '/commands/')
		user, host = uhost.split('!')
		user = user[1:]
		message = [x for x in message]
		message = [message[0][1:]] + message[1:]
		
		if channel == self.botname:
			channel = user
		
		self.prout('{3}[{0}{4} {5}{1}{4}{3}]{4} {2}'.format(channel if channel != user else 'PM from', user, ' '.join(message),tc['bold'],tc['end'],tc['warning']))
		
		if message[0].startswith(self.botcmd):
			command = message[0][len(self.botcmd):]
			params = message[1:]
			
			cmd = self.is_command(command)
			
			if cmd == 0:
				cmd = 'ahk'
				params = [message[0][len(self.botcmd):]] + message[1:]
				print( params )
			response = self.commands[cmd].execute(self, self.commands, self.irc, user, host, channel, params)
			for re in response:
				self.irc.privmsg(channel, re.replace('&botcmd', self.botcmd))
		return 0
	
	def sys_message(self, message):
		self.prout(message)
		return 0
	
	def is_command(self, command):
		for cm in self.commands:
			if any( command == c for c in self.commands[cm].meta_data['aliases'] ):
				return cm
		return 0

if __name__ == '__main__':
	sjbot = sjBot('irc.freenode.net', 6667)
