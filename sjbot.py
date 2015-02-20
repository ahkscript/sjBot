import bot
import json
import time
import sys
import os


botcmd = '`'
default_dir = os.path.dirname(os.path.realpath(__file__))
owners = ['/sjc1000','180.181.27.230', 'Sjc1000@gateway/shell/elitebnc']

def onALL(bot, msg, *params):
	plugins = bot.load_plugins(default_dir + '/plugins/', 'plg_')
	for plugin in plugins:
		if hasattr(plugins[plugin], 'on' + msg):
			getattr(plugins[plugin], 'on' + msg)(bot, *params)
	return 0

def is_command(commands, command):
	for cmd in commands:
		if any( command == cm for cm in commands[cmd].meta_data['aliases'] ):
			return 1
	return 0

def onSTART(bot, *params):
	bot.ident('sjBot')
	return 0

def on376(bot, *params):
	bot.irc.privmsg('NickServ', 'Identify sjBot ' + keys['sjbot_pass'])
	return 0

def on433(bot, host, ast, nickname, *params):
	bot.irc.nick(nickname + '_')

def on396(bot, *params):
	bot.irc.join(['#Sjc_Bot', '#ahkscript', '#ahk'])
	return 0

def onPRIVMSG(bot, full_host, channel, *message):
	commands = bot.load_plugins(default_dir + '/commands/', 'cmd_')
	message = ' '.join(message)[1:].split(' ')
	user = full_host.split('!')[0]
	host = full_host.split('!')[1]
	if message[0].startswith(botcmd):
		if is_command(commands, message[0][1:]):
			command = message[0][1:]
			params = message[1:]
		else:
			command = 'ahk'
			params = ' '.join(message)[1:].split(' ')
		
		if commands[command].meta_data['owner'] == 1 and not any( host in full_host for host in owners ):
			bot.irc.privmsg(channel, 'You are not an owner!')
			return 0
		response = commands[command].execute(bot, commands, user, full_host, channel, params)
		if response == 0:
			return 0
		
		if response['Status'] == -1:
			if isinstance(response['Text'], list):
				for line in response['Text']:
					bot.irc.privmsg(channel, '[' + response['Error'] + '] ' + line.replace('&botcmd', botcmd))
			else:
				bot.irc.privmsg(channel, '[' + response['Error'] + '] ' + response['Text'].replace('&botcmd', botcmd))
		else:
			if isinstance(response['Text'], list):
				for line in response['Text']:
					bot.irc.privmsg(channel, line.replace('&botcmd', botcmd))
			else:
				bot.irc.privmsg(channel, response['Text'].replace('&botcmd', botcmd))
	return 0


with open(default_dir + '/keys') as my_file:
	keys = json.loads( my_file.read() )

if __name__ == '__main__':

	while True:
		sjBot = bot._bot('irc.freenode.net', 6667, os.path.realpath(__file__))
		sjBot.botcmd = botcmd
		sjBot.keys = keys
		commands = sjBot.load_plugins(default_dir + '/commands/', 'cmd_')
		plugins = sjBot.load_plugins(default_dir + '/plugins/', 'plg_')
		sjBot.main_loop()
		time.sleep(10)
