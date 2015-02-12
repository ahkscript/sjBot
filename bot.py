import irc
import threads
import plugins
import time
import sys
import os
import json
import random
import urllib.request

class bot():
	botname = 'sjBot'
	server = 'irc.freenode.net'
	port = 6667
	botcmd = ['`', botname + ':']
	ownerlist = ['/sjc1000','180.181.27.230', 'Sjc1000@gateway/shell/elitebnc']
	ignorelist = ['geekbot', 'forumbot']
	ignorecommands = [',', 'n', 'r', '.', '::']
	default_dir = os.path.dirname(os.path.realpath(__file__))
	commands_dir = default_dir + '/commands/'
	plugins_dir = default_dir + '/plugins/'
	channel_list = ['#Sjc_Bot', "#ahkscript", "#ahk"]

	def __init__(self):
		self.thread = threads.thread()
		self.irc = irc.client(self.server, self.port)
		self.irc.ident(self.botname)
		self.commands = plugins.plugin(self.default_dir + '/commands/')
		self.plugins = plugins.plugin(self.default_dir + '/plugins/')
		self.thread.add_task('update_plugins', [20], self)
		
		with open(self.default_dir + '/keys') as my_file:
			self.keys = json.loads(my_file.read())

	def update_plugins(self, timeout):
		while True:
			time.sleep(timeout)
			self.commands.load_plugins()
			self.plugins.load_plugins()
			self.thread.add_task('call_plugin', ['UPDATE', 'data'], self)
		return 0

	def download_url(self, url):
		try:
			response = urllib.request.urlopen(url)
			response_data = response.read().decode('utf-8')
		except UnicodeDecodeError:
			raise UnicodeDecodeError('response.read().decode()')
		return response_data
	
	def shorten_url(self, url):
		return self.download_url('https://api-ssl.bitly.com/v3/shorten?access_token=' + self.keys['bitly'] + '&format=txt&Longurl=' + url)
		

	def main_loop(self):
		self.previous_data = b''
		while True:
			try:
				recieved = self.irc.recv()
			except UnicodeDecodeError:
				print('! Decode Error. Skipping current data and waiting for more.')
				continue
			if len(recieved) == 0:
				print('! Host closed the connection, shuting down sockets and rebooting.')
				self.irc.stop()
				break
			if recieved.endswith(b'\r\n'):
				try:
					self.handle_data(self.previous_data + recieved)
				except UnicodeDecodeError:
					continue
				self.previous_data = b''
			else:
				self.previous_data = self.previous_data + recieved

		print('| Bot has stopped.')
		return self.channel_list

	def handle_data(self, data):
		for line in data.decode('utf-8').split('\r\n'):
			if line != '':
				print('> ' + line)
				split = line.split(' ')

				if split[0] == "PING":
					self.irc.pong(split[1][1:])

				if len(split) > 2:
					params = [ split[0][1:] ] + split[2:]
					self.thread.add_task('on' + split[1], params, self)
					self.thread.add_task('call_plugin', [split[1], line], self)
		return 0

	def call_plugin(self, plugin, data):
		plugin_list = self.plugins.plugins
		for pl in plugin_list:
			self.plugins.run_plugin(pl, 'on' + plugin, [self, data])
		return 0

	def on376(self, host, botname, *junk):
		with open(self.default_dir + '/password', 'r') as my_file:
			password = my_file.read()
			self.irc.privmsg('NickServ', 'Identify ' + self.botname + ' ' + password)
		return 0

	def on396(self, host, botname, newhost, *junk):
		self.irc.join(self.channel_list)
		return 0

	def on433(self, server, a, nickname, *junk):
		self.botname = nickname + '_'
		self.irc.send('NICK ' + self.botname)
		return 0

	def onNOTICE(self, host, botname, *message):
		if host == 'NickServ!NickServ@services.' and 'not a registered' in ' '.join(message):
			self.irc.join(self.channel_list)
		return 0

	def onJOIN(self, host, channel):
		if channel not in self.channel_list:
			self.channel_list.append(channel)

		if self.botname == host.split('!')[0]:
			time.sleep(5)
			self.irc.privmsg(channel, 'Hello World!')
		return 0

	def onPART(self, host, channel, *junk):
		if channel in self.channel_list:
			self.channel_list.remove(channel)
		return 0

	def onINVITE(self, user, nickname, channel):
		self.irc.join([channel[1:]])
		return 0

	def onPRIVMSG(self, host, channel, *message):
		message = list(message)
		message = [message[0][1:]] + message[1:]

		for cmd in self.botcmd:
			if message[0][:len(cmd)] == cmd:
				if self.botname in cmd:
					command = message[1:]
				else:
					command = [message[0][1:]] + message[1:]
				if command[0] in self.ignorecommands:
					return 0

				print('| Command recieved ' + command[0])
				for pl in self.commands.plugins:
					for cm in self.commands.plugins[pl].metaData['aliases']:
						if cm == command[0]:
							self.call_command(pl.lower(), command[1:], host.split('!')[0], channel, host)
							return 0
				self.call_command(command[0].lower(), command[1:], host.split('!')[0], channel, host)
				return 0
		return 0
	
	def call_command(self, command, params, user, channel, host):
		if channel == self.botname:
			channel = user

		if command.count(self.botcmd[0]) == len(command):
			return 0

		
		if self.is_command(command):
			if self.commands.plugins[command].metaData['owner'] == 1 and self.is_owner(host) == 0:
				self.irc.privmsg(channel, 'Sorry ' + user + ', you are not permitted to use that command.')
				return 0
			response_data = self.commands.run(command, [(command, self.commands.plugins, self.botcmd, self.is_owner(host), self.irc, self), user, host, channel, params])
		else:
			response_data = self.commands.run('ahk', [(command, self.commands.plugins, self.botcmd, self.is_owner(host), self.irc, self), user, host, channel, [command] + params])

		if isinstance(response_data, int):
			return 0

		if isinstance( response_data, str):
			self.irc.privmsg(channel, response_data.replace('&botcmd', self.botcmd[0]))
		else:
			for send in response_data:
				self.irc.privmsg(channel, send.replace('&botcmd', self.botcmd[0]))
		return 0

	def is_command(self, command):
		for cmd in self.commands.plugins:
			for alias in self.commands.plugins[cmd].metaData['aliases']:
				if command == alias:
					return 1
		return 0


	def is_owner(self, host):
		return any(chost in host for chost in self.ownerlist)



channels = []
if __name__ == '__main__':
	while True:
		sjBot = bot()
		if channels != []:
			sjBot.channel_list = channels
		channels = sjBot.main_loop()
		time.sleep(10)
