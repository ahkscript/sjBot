

import time


def onJOIN(parent, host, join, channel):
	user = host.split('!')[0][1:]
	channel = channel[1:]
	if user == parent.nickname:
		return None
	time.sleep(1)
	parent.privmsg(channel, 'Welcome to ' + channel + ' ' + user + '. Use .help for a list of commands.')
	return None