def onJOIN(sjBot, host, join, channel):
	if host.split('!')[0][1:] == 'maestrith':
		sjBot.action(channel, 'bows')
	return None