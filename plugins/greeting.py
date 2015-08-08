#!/usr/bin/env python3


import random


greetings = ['hi', 'hello', 'howdy', 'heya', 'sup', 'wassup', 'hey']
replace = ['.', ',']


def onPRIVMSG(this, host, privmsg, channel, *message):
	if len(message) < 2:
		return None
	if message[0][1:].lower() in greetings and this.nickname == message[1].replace(',','').replace('.',''):
		nick = host.split('!')[0][1:]

		if nick == this.last_greeting:
			return None

		response = random.choice(greetings)
		response = response[0].upper() + response[1:]
		this.privmsg(channel, response + ' ' + nick + '.')
		this.last_greeting = nick
	return None